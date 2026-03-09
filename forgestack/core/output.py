from __future__ import annotations

import json
from pathlib import Path


class ConsoleRenderer:
    def render_plan(self, plan, stack, plugins: list[str]) -> str:
        lines = [f"ForgeStack plan for '{stack.name}'", "", f"Plugins: {', '.join(plugins)}", "", "Plan:"]
        if not plan.actions:
            lines.append("  (no actions)")
        for action in plan.actions:
            target = action.path or action.payload.get("name", "")
            lines.append(f"  + {action.kind}: {target}".rstrip())
        if plan.warnings:
            lines.extend(["", "Warnings:"])
            lines.extend([f"  - {warning}" for warning in plan.warnings])
        return "\n".join(lines)

    def render_apply_summary(self, stack, plugins: list[str], result, workspace_root: Path) -> str:
        return "\n".join([
            f"ForgeStack applied stack '{stack.name}'",
            f"Workspace: {workspace_root}",
            f"Plugins: {', '.join(plugins)}",
            f"Files written: {len(result.written_files)}",
            f"Commands executed: {len(result.executed_commands)}",
        ])


class JsonRenderer:
    def render_plan(self, plan, stack, plugins: list[str]) -> str:
        payload = {"stack": stack.name, "plugins": plugins, **plan.to_dict()}
        return json.dumps(payload, indent=2)

    def render_graph(self, graph, ordered_plugins: list[str]) -> str:
        payload = {
            "ordered_plugins": ordered_plugins,
            "nodes": {name: {"requires": sorted(graph.edges.get(name, set()))} for name in graph.nodes},
        }
        return json.dumps(payload, indent=2)
