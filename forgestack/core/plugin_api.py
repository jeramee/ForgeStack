# NOTE:
# This plugin API supports both legacy plugin planning and a richer parallel
# composition path. The current authoritative public `devmake apply` path uses
# simple plugin `plan(ctx)` behavior through `forgestack/core/planner.py`.
# Keep new public apply behavior out of the richer `contribute()` / PlanAction
# path unless intentionally migrating the active public path.
# forgestack/core/plugin_api.py

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .models import PluginConfig, PluginContribution, StackConfig


@dataclass(slots=True)
class PluginMetadata:
    name: str
    version: str = "0.1.0"
    requires: list[str] = field(default_factory=list)
    provides: list[str] = field(default_factory=list)
    description: str = ""
    compatible_core: str = ">=0.1.0"


class Plugin(ABC):
    metadata: PluginMetadata

    def __init__(self, name: str | None = None, requires: list[str] | None = None):
        if name is not None:
            self.metadata = PluginMetadata(
                name=name,
                requires=requires or [],
            )
        elif not hasattr(self, "metadata"):
            raise TypeError(
                f"{self.__class__.__name__} must define 'metadata' "
                "or call super().__init__(name, requires)"
            )

    @property
    def name(self) -> str:
        return self.metadata.name

    @property
    def requires(self) -> list[str]:
        return self.metadata.requires

    @property
    def provides(self) -> list[str]:
        return self.metadata.provides

    def before_generate(self, ctx: "PluginContext") -> None:
        return None

    def plan(self, ctx: "PluginContext"):
        raise NotImplementedError

    def contribute(self, ctx: "PluginContext") -> PluginContribution:
        raise NotImplementedError(
            f"Plugin '{self.name}' does not implement contribute() yet"
        )

    def after_generate(self, ctx: "PluginContext") -> None:
        return None


@dataclass
class PluginContext:
    stack_config: StackConfig
    plugin_config: PluginConfig
    planner: Any
    workspace_root: str = "."
    interactive: bool = True
    capabilities: set[str] = field(default_factory=set)
    env: dict[str, str] = field(default_factory=dict)

    @property
    def plugin_name(self) -> str:
        return self.plugin_config.name

    @property
    def cfg(self) -> dict[str, Any]:
        return self.stack_config.raw

    @property
    def options(self) -> dict[str, Any]:
        return self.plugin_config.options

    @property
    def root(self) -> Path:
        return Path(self.workspace_root)

    def create_dir(self, path: str, description: str = "") -> None:
        from .plan import PlanAction
        self.planner.add_action(
            PlanAction(
                kind="create_dir",
                path=path,
                plugin=self.plugin_name,
                description=description,
            )
        )

    def create_file(self, path: str, content: str, description: str = "") -> None:
        from .plan import PlanAction
        self.planner.add_action(
            PlanAction(
                kind="create_file",
                path=path,
                plugin=self.plugin_name,
                payload={"content": content},
                description=description,
            )
        )

    def update_file(self, path: str, content: str, description: str = "") -> None:
        from .plan import PlanAction
        self.planner.add_action(
            PlanAction(
                kind="update_file",
                path=path,
                plugin=self.plugin_name,
                payload={"content": content},
                description=description,
            )
        )

    def append_file(self, path: str, text: str, description: str = "") -> None:
        from .plan import PlanAction
        self.planner.add_action(
            PlanAction(
                kind="append_file",
                path=path,
                plugin=self.plugin_name,
                payload={"content": text},
                description=description,
            )
        )

    def patch_file(
        self,
        path: str,
        pattern: str,
        replacement: str,
        description: str = "",
    ) -> None:
        from .plan import PlanAction
        self.planner.add_action(
            PlanAction(
                kind="patch_file",
                path=path,
                plugin=self.plugin_name,
                payload={"pattern": pattern, "replacement": replacement},
                description=description,
            )
        )

    def add_service(self, name: str, config: dict[str, Any], description: str = "") -> None:
        from .plan import PlanAction
        self.planner.add_action(
            PlanAction(
                kind="add_service",
                plugin=self.plugin_name,
                payload={"name": name, "config": config},
                description=description,
            )
        )

    def run_command(self, cmd: list[str], cwd: str = ".", description: str = "") -> None:
        from .plan import PlanAction
        self.planner.add_action(
            PlanAction(
                kind="run_command",
                plugin=self.plugin_name,
                payload={"cmd": cmd, "cwd": cwd},
                description=description,
            )
        )
