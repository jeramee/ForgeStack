# NOTE:
# This module is part of a richer parallel composition path that is not the
# current authoritative public `devmake apply` path.
# Public generation behavior currently flows through:
# cli/main.py -> stack_loader.py -> preset_resolver.py -> registry.py
# -> planner.py -> plan_executor.py
# Keep new public apply behavior out of this module unless intentionally migrating.
from __future__ import annotations

from .models import FileSpec, PluginContribution, StackModel, TaskSpec
from .plan import PlanBuilder
from .plugin_api import PluginContext


class StackComposer:
    """
    Compose requested plugins into a canonical in-memory stack model.

    New plugins should implement contribute(ctx) -> PluginContribution.
    Legacy plugins that only implement plan(ctx) are adapted through the
    existing planner actions so ForgeStack can migrate gradually.
    """

    def compose(self, stack_config, ordered_plugins: list[str], registry, interactive: bool = True) -> StackModel:
        plugin_configs = {plugin.name: plugin for plugin in stack_config.plugins}
        model = StackModel(
            name=stack_config.name,
            requested_plugins=stack_config.plugin_names(),
            resolved_plugins=list(ordered_plugins),
        )
        file_owners: dict[str, str] = {}

        for plugin_name in ordered_plugins:
            plugin = registry.load(plugin_name)
            plugin_cfg = plugin_configs.get(plugin_name)
            if plugin_cfg is None:
                from .models import PluginConfig
                plugin_cfg = PluginConfig(name=plugin_name)

            ctx = PluginContext(
                stack_config=stack_config,
                plugin_config=plugin_cfg,
                planner=PlanBuilder(),
                workspace_root=stack_config.name,
                interactive=interactive,
                capabilities=set(model.capabilities),
                env=dict(model.env),
            )

            contribution = self._get_contribution(plugin, ctx)
            self._merge_contribution(model, contribution, file_owners)

        return model

    def _get_contribution(self, plugin, ctx: PluginContext) -> PluginContribution:
        contribute_impl = getattr(type(plugin), "contribute", None)
        if contribute_impl is not None and contribute_impl is not getattr(__import__("forgestack.core.plugin_api", fromlist=["Plugin"]).Plugin, "contribute"):
            return plugin.contribute(ctx)
        return self._legacy_plugin_to_contribution(plugin, ctx)

    def _legacy_plugin_to_contribution(self, plugin, ctx: PluginContext) -> PluginContribution:
        plan_builder = PlanBuilder()
        legacy_ctx = PluginContext(
            stack_config=ctx.stack_config,
            plugin_config=ctx.plugin_config,
            planner=plan_builder,
            workspace_root=ctx.workspace_root,
            interactive=ctx.interactive,
            capabilities=set(ctx.capabilities),
            env=dict(ctx.env),
        )
        plugin.before_generate(legacy_ctx)
        maybe_plan = plugin.plan(legacy_ctx)
        if maybe_plan is not None:
            plan_builder.add_legacy_plan(plugin.name, maybe_plan)
        plugin.after_generate(legacy_ctx)

        contribution = PluginContribution(
            plugin_name=plugin.name,
            provides=set(getattr(plugin, "provides", []) or []),
            requires=set(getattr(plugin, "requires", []) or []),
        )

        for action in plan_builder.actions:
            if action.kind == "create_file":
                contribution.files.append(
                    FileSpec(
                        path=action.path or "",
                        content=action.payload.get("content", ""),
                        mode="replace",
                        owner=plugin.name,
                    )
                )
            elif action.kind == "update_file":
                contribution.files.append(
                    FileSpec(
                        path=action.path or "",
                        content=action.payload.get("content", ""),
                        mode="replace",
                        owner=plugin.name,
                    )
                )
            elif action.kind == "append_file":
                contribution.files.append(
                    FileSpec(
                        path=action.path or "",
                        content=action.payload.get("content", ""),
                        mode="append",
                        owner=plugin.name,
                    )
                )
            elif action.kind == "add_service":
                from .models import ServiceSpec
                name = action.payload.get("name")
                if isinstance(name, str) and name.startswith("volume:"):
                    continue
                cfg = action.payload.get("config", {}) or {}
                contribution.services[name] = ServiceSpec(
                    name=name,
                    kind=cfg.get("kind", "service"),
                    image=cfg.get("image"),
                    build_context=cfg.get("build"),
                    command=cfg.get("command", []) or [],
                    ports=cfg.get("ports", []) or [],
                    env=cfg.get("environment", cfg.get("env", {})) or {},
                    depends_on=cfg.get("depends_on", []) or [],
                    volumes=cfg.get("volumes", []) or [],
                )
            elif action.kind == "run_command":
                task_name = f"{plugin.name}:command:{len(contribution.tasks)+1}"
                contribution.tasks[task_name] = TaskSpec(
                    name=task_name,
                    command=list(action.payload.get("cmd", [])),
                    cwd=action.payload.get("cwd") or ".",
                )

        return contribution

    def _merge_contribution(self, model: StackModel, contribution: PluginContribution, file_owners: dict[str, str]) -> None:
        model.capabilities.update(contribution.provides)
        model.warnings.extend(contribution.warnings)
        model.env.update(contribution.env)
        model.packages.extend(contribution.packages)

        for service_name, service in contribution.services.items():
            if service_name in model.services:
                raise RuntimeError(
                    f"Service conflict: '{service_name}' declared by both "
                    f"'{model.services[service_name].name}' and '{contribution.plugin_name}'"
                )
            model.services[service_name] = service

        for file in contribution.files:
            owner = file_owners.get(file.path)
            if owner and owner != contribution.plugin_name and file.mode == "replace":
                raise RuntimeError(
                    f"File conflict: '{file.path}' owned by both '{owner}' and '{contribution.plugin_name}'"
                )
            file_owners[file.path] = contribution.plugin_name
            model.files.append(file)

        for task_name, task in contribution.tasks.items():
            if task_name in model.tasks:
                raise RuntimeError(f"Task conflict: '{task_name}' declared by multiple plugins")
            model.tasks[task_name] = task
