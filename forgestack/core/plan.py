# NOTE:
# This plan model supports a richer parallel planning path and is not the
# current authoritative public plan used by `devmake apply`.
# The active public path currently uses `forgestack/core/planner.py`
# together with `forgestack/core/plan_executor.py`.
# Keep new public behavior out of this module unless intentionally migrating.
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

from .graph import DependencyGraph, GraphBuilder, GraphSorter
from .plugin_api import PluginContext
from .registry import RegistryManager

ActionKind = Literal[
    "create_dir",
    "create_file",
    "update_file",
    "append_file",
    "patch_file",
    "add_service",
    "run_command",
]


@dataclass(slots=True)
class PlanAction:
    kind: ActionKind
    path: str | None = None
    plugin: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    description: str = ""


@dataclass(slots=True)
class Plan:
    actions: list[PlanAction] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    diagnostics: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "actions": [asdict(action) for action in self.actions],
            "warnings": list(self.warnings),
            "diagnostics": list(self.diagnostics),
        }


@dataclass
class PlanBuilder:
    actions: list[PlanAction] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    diagnostics: list[str] = field(default_factory=list)

    def add_action(self, action: PlanAction) -> None:
        self.actions.append(action)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def info(self, message: str) -> None:
        self.diagnostics.append(message)

    def add_legacy_plan(self, plugin_name: str, legacy_plan: Any) -> None:
        if legacy_plan is None:
            return
        for folder in getattr(legacy_plan, "folders", []):
            self.add_action(PlanAction(kind="create_dir", path=folder, plugin=plugin_name, description=f"Create directory {folder}"))
        for file_write in getattr(legacy_plan, "files", []):
            self.add_action(PlanAction(kind="create_file", path=file_write.path, plugin=plugin_name, payload={"content": file_write.content}, description=f"Create file {file_write.path}"))
        compose = getattr(legacy_plan, "compose", None) or {}
        for service_name, service_cfg in compose.get("services", {}).items():
            self.add_action(PlanAction(kind="add_service", plugin=plugin_name, payload={"name": service_name, "config": service_cfg}, description=f"Add service {service_name}"))
        for volume_name, volume_cfg in compose.get("volumes", {}).items():
            self.add_action(PlanAction(kind="add_service", plugin=plugin_name, payload={"name": f"volume:{volume_name}", "config": volume_cfg, "section": "volumes"}, description=f"Add volume {volume_name}"))
        for command in getattr(legacy_plan, "commands", []):
            self.add_action(PlanAction(kind="run_command", plugin=plugin_name, payload={"cmd": command.cmd, "cwd": command.cwd}, description=f"Run command {' '.join(command.cmd)}"))

    def build(self) -> Plan:
        return Plan(actions=self.actions, warnings=self.warnings, diagnostics=self.diagnostics)


# legacy compatibility for older plugin imports
@dataclass
class FileWrite:
    path: str
    content: str


@dataclass
class Command:
    cmd: list[str]
    cwd: str = "."


@dataclass
class LegacyPlan:
    folders: list[str] = field(default_factory=list)
    files: list[FileWrite] = field(default_factory=list)
    commands: list[Command] = field(default_factory=list)
    compose: dict[str, Any] = field(default_factory=dict)


class DefaultPlanner:
    def __init__(self) -> None:
        self.graph_builder = GraphBuilder()
        self.sorter = GraphSorter()

    def _resolve_dependencies(self, requested: list[str], registry: RegistryManager) -> list[str]:
        resolved: list[str] = []
        seen: set[str] = set()

        def visit(name: str) -> None:
            if name in seen:
                return
            seen.add(name)
            plugin = registry.load(name)
            for dep in plugin.requires:
                visit(dep)
            resolved.append(name)

        for plugin_name in requested:
            visit(plugin_name)
        return resolved

    def create_plan(self, stack_config, registry: RegistryManager) -> tuple[DependencyGraph, list[str], Plan]:
        requested = stack_config.plugin_names()
        resolved = self._resolve_dependencies(requested, registry)
        graph = self.graph_builder.build(resolved, registry)
        ordered_plugins = self.sorter.topo_sort(graph)
        plan_builder = PlanBuilder()
        plugin_configs = {plugin.name: plugin for plugin in stack_config.plugins}

        for plugin_name in ordered_plugins:
            plugin = registry.load(plugin_name)
            plugin_cfg = plugin_configs.get(plugin_name)
            if plugin_cfg is None:
                from .models import PluginConfig
                plugin_cfg = PluginConfig(name=plugin_name)
            ctx = PluginContext(stack_config=stack_config, plugin_config=plugin_cfg, planner=plan_builder, workspace_root=stack_config.name)
            plugin.before_generate(ctx)
            maybe_plan = plugin.plan(ctx)
            if maybe_plan is not None:
                plan_builder.add_legacy_plan(plugin_name, maybe_plan)
            plugin.after_generate(ctx)

        return graph, ordered_plugins, plan_builder.build()
