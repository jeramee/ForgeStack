from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .models import StackModel
from .plan import Plan
from .renderers.docker_compose import DockerComposeRenderer
from .renderers.docs import DocsRenderer
from .renderers.env import EnvRenderer
from .renderers.filesystem import FilesystemRenderer


@dataclass(slots=True)
class WrittenFile:
    path: str
    plugin: str | None


@dataclass(slots=True)
class ApplyResult:
    written_files: list[WrittenFile] = field(default_factory=list)
    executed_commands: list[list[str]] = field(default_factory=list)


class DefaultExecutor:
    def apply(self, plan: Plan, workspace_root: str | Path, run_commands: bool = True) -> ApplyResult:
        root = Path(workspace_root)
        root.mkdir(parents=True, exist_ok=True)
        result = ApplyResult()

        compose_services: dict[str, Any] = {}
        compose_volumes: dict[str, Any] = {}
        commands: list[tuple[list[str], str]] = []

        for action in plan.actions:
            if action.kind == "create_dir":
                if action.path:
                    (root / action.path).mkdir(parents=True, exist_ok=True)

            elif action.kind in {"create_file", "update_file"}:
                if action.path:
                    target = root / action.path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(action.payload.get("content", ""), encoding="utf-8")
                    result.written_files.append(WrittenFile(path=action.path, plugin=action.plugin))

            elif action.kind == "append_file":
                if action.path:
                    target = root / action.path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    existing = target.read_text(encoding="utf-8") if target.exists() else ""
                    addition = action.payload.get("content", "")
                    if addition not in existing:
                        target.write_text(existing + addition, encoding="utf-8")
                    result.written_files.append(WrittenFile(path=action.path, plugin=action.plugin))

            elif action.kind == "patch_file":
                if action.path:
                    target = root / action.path
                    content = target.read_text(encoding="utf-8") if target.exists() else ""
                    updated = re.sub(
                        action.payload.get("pattern", ""),
                        action.payload.get("replacement", ""),
                        content,
                        flags=re.MULTILINE,
                    )
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(updated, encoding="utf-8")
                    result.written_files.append(WrittenFile(path=action.path, plugin=action.plugin))

            elif action.kind == "add_service":
                name = action.payload.get("name")
                config = action.payload.get("config", {})
                section = action.payload.get("section", "services")
                if section == "volumes" or (isinstance(name, str) and name.startswith("volume:")):
                    volume_name = name.split(":", 1)[1] if isinstance(name, str) and name.startswith("volume:") else name
                    compose_volumes[volume_name] = config
                else:
                    compose_services[name] = config

            elif action.kind == "run_command":
                commands.append((list(action.payload.get("cmd", [])), action.payload.get("cwd", ".")))

            else:
                raise ValueError(f"Unsupported action kind: {action.kind}")

        if compose_services or compose_volumes:
            compose = {"version": "3.9", "services": compose_services}
            if compose_volumes:
                compose["volumes"] = compose_volumes
            compose_path = root / "docker-compose.yml"
            compose_path.write_text(yaml.safe_dump(compose, sort_keys=False), encoding="utf-8")
            result.written_files.append(WrittenFile(path="docker-compose.yml", plugin="forgestack"))

        if run_commands:
            for cmd, cwd in commands:
                if not cmd:
                    continue
                subprocess.run(cmd, cwd=root / cwd, check=False)
                result.executed_commands.append(cmd)

        return result

    def apply_model(self, model: StackModel, workspace_root: str | Path, render_docs: bool = True) -> ApplyResult:
        root = Path(workspace_root)
        root.mkdir(parents=True, exist_ok=True)

        FilesystemRenderer().render(model, str(root))
        DockerComposeRenderer().render(model, str(root))
        EnvRenderer().render(model, str(root))
        if render_docs:
            DocsRenderer().render(model, str(root))

        result = ApplyResult()
        for file in model.files:
            result.written_files.append(WrittenFile(path=file.path, plugin=file.owner))
        result.written_files.append(WrittenFile(path="docker-compose.yml", plugin="forgestack"))
        result.written_files.append(WrittenFile(path=".env.example", plugin="forgestack"))
        if render_docs:
            result.written_files.append(WrittenFile(path="STACK.md", plugin="forgestack"))
        return result
