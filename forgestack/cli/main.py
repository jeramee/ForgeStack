import argparse
from pathlib import Path

from forgestack.core.registry import PluginRegistry
from forgestack.core.planner import create_plan
from forgestack.core.stack_loader import (
    load_stack_yaml,
    detect_kind,
)
from forgestack.core.preset_resolver import resolve_document
from forgestack.core.plan_executor import execute_plan


def resolve_project_name(doc):
    kind = detect_kind(doc)

    if kind == "project":
        name = doc.get("name")
        if name:
            return name

    if kind == "resolved-project":
        name = doc.get("name")
        if name:
            return name

    project = doc.get("project", {})
    if isinstance(project, dict):
        name = project.get("name")
        if name:
            return name

    name = doc.get("name")
    if name:
        return name

    return "MyApp"


def get_plugin_names(doc):
    plugins = doc.get("plugins", [])

    if not isinstance(plugins, list):
        raise RuntimeError("'plugins' must be a list")

    return plugins


def cmd_plan(args):
    raw_doc = load_stack_yaml(args.stack)
    effective_doc = resolve_document(raw_doc)
    plugin_names = get_plugin_names(effective_doc)

    registry = PluginRegistry()
    registry.discover()

    graph, plan = create_plan(plugin_names, registry)

    print("\nDocument kind:", detect_kind(raw_doc))
    if detect_kind(raw_doc) == "project":
        print("Resolved kind:", effective_doc.get("kind"))

    print("Requested:", plugin_names)
    print("Resolved:", sorted(graph.nodes.keys()))

    print("\nExecution Plan:")
    for action in plan.actions:
        print("-", action)


def cmd_graph(args):
    raw_doc = load_stack_yaml(args.stack)
    effective_doc = resolve_document(raw_doc)
    plugin_names = get_plugin_names(effective_doc)

    registry = PluginRegistry()
    registry.discover()

    graph, _ = create_plan(plugin_names, registry)

    print("\nDocument kind:", detect_kind(raw_doc))
    if detect_kind(raw_doc) == "project":
        print("Resolved kind:", effective_doc.get("kind"))

    print("Dependency Graph:")
    for node, deps in graph.edges.items():
        print(node, "->", list(deps))


def cmd_apply(args):
    raw_doc = load_stack_yaml(args.stack)
    effective_doc = resolve_document(raw_doc)
    plugin_names = get_plugin_names(effective_doc)

    registry = PluginRegistry()
    registry.discover()

    _, plan = create_plan(plugin_names, registry)

    project_name = resolve_project_name(effective_doc)
    output_root = Path("output") / project_name

    print(f"\nApplying ForgeStack Plan into: {output_root}\n")
    execute_plan(plan, output_root=output_root)


def cmd_plugins(args):
    registry = PluginRegistry()
    registry.discover()

    print("\nInstalled Plugins:\n")
    for name in registry.list():
        print("-", name)


def main():
    parser = argparse.ArgumentParser(prog="devmake")
    sub = parser.add_subparsers(dest="command")

    plan_cmd = sub.add_parser("plan")
    plan_cmd.add_argument("stack")
    plan_cmd.set_defaults(func=cmd_plan)

    graph_cmd = sub.add_parser("graph")
    graph_cmd.add_argument("stack")
    graph_cmd.set_defaults(func=cmd_graph)

    apply_cmd = sub.add_parser("apply")
    apply_cmd.add_argument("stack")
    apply_cmd.set_defaults(func=cmd_apply)

    plugins_cmd = sub.add_parser("plugins")
    plugins_cmd.set_defaults(func=cmd_plugins)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)


def run_cli():
    return main()