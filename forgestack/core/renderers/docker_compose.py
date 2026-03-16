from __future__ import annotations

from pathlib import Path
import yaml

from ..models import StackModel


class DockerComposeRenderer:
    def render(self, model: StackModel, root: str) -> None:
        compose: dict = {"services": {}}
        volumes: dict[str, dict] = {}

        for name, service in model.services.items():
            spec: dict = {}

            # Preferred stable output order
            if getattr(service, "image", None):
                spec["image"] = service.image
            if getattr(service, "build_context", None):
                spec["build"] = service.build_context
            if getattr(service, "working_dir", None):
                spec["working_dir"] = service.working_dir
            if getattr(service, "volumes", None):
                spec["volumes"] = service.volumes
                for vol in service.volumes:
                    if ":" in vol:
                        vol_name = vol.split(":", 1)[0]
                        if (
                            "/" not in vol_name
                            and "\\" not in vol_name
                            and not vol_name.startswith(".")
                        ):
                            volumes[vol_name] = {}
            if getattr(service, "ports", None):
                spec["ports"] = service.ports
            if getattr(service, "env", None):
                spec["environment"] = service.env
            if getattr(service, "command", None):
                spec["command"] = service.command
            if getattr(service, "depends_on", None):
                spec["depends_on"] = service.depends_on

            compose["services"][name] = spec

        if volumes:
            compose["volumes"] = volumes

        out = Path(root) / "docker-compose.yml"
        out.write_text(
            yaml.safe_dump(
                compose,
                sort_keys=False,
                default_flow_style=False,
            ),
            encoding="utf-8",
        )