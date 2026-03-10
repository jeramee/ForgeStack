import argparse
import sys
from pathlib import Path

import yaml

from forgestack.config.validators import ValidationError
from forgestack.core.registry import PluginRegistry
from forgestack.core.planner import create_plan
from forgestack.core.stack_loader import (
    load_stack_yaml,
    detect_kind,
    resolve_project_name,
    get_plugin_names,
)
from forgestack.core.preset_resolver import resolve_document
from forgestack.core.plan_executor import execute_plan


def _run_safely(fn):
    try:
        return fn()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        raise SystemExit(1)
    except ValidationError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        raise SystemExit(1)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        raise SystemExit(1)


def _build_render_context(raw_doc, effective_doc):
    plugins = get_plugin_names(effective_doc)

    return {
        "raw": raw_doc,
        "effective": effective_doc,
        "project": effective_doc.get("project", raw_doc),
        "project_name": resolve_project_name(effective_doc),
        "stack": effective_doc.get("stack", {}),
        "app": effective_doc.get("app", {}),
        "values": effective_doc.get("values", {}),
        "plugins": plugins,
        "has_plugin": {name: True for name in plugins},
    }


def _list_yaml_stems(folder: Path) -> list[str]:
    if not folder.exists():
        return []
    return sorted(p.stem for p in folder.glob("*.yaml"))


def cmd_plan(args):
    def _inner():
        raw_doc = load_stack_yaml(args.stack)
        effective_doc = resolve_document(raw_doc)
        plugin_names = get_plugin_names(effective_doc)
        render_context = _build_render_context(raw_doc, effective_doc)

        registry = PluginRegistry()
        registry.discover()

        graph, plan = create_plan(plugin_names, registry, render_context=render_context)

        print("\nDocument kind:", detect_kind(raw_doc))
        if detect_kind(raw_doc) == "project":
            print("Resolved kind:", effective_doc.get("kind"))

        print("Requested:", plugin_names)
        print("Resolved:", sorted(graph.nodes.keys()))

        print("\nExecution Plan:")
        for action in plan.actions:
            print("-", action)

    _run_safely(_inner)


def cmd_graph(args):
    def _inner():
        raw_doc = load_stack_yaml(args.stack)
        effective_doc = resolve_document(raw_doc)
        plugin_names = get_plugin_names(effective_doc)
        render_context = _build_render_context(raw_doc, effective_doc)

        registry = PluginRegistry()
        registry.discover()

        graph, _ = create_plan(plugin_names, registry, render_context=render_context)

        print("\nDocument kind:", detect_kind(raw_doc))
        if detect_kind(raw_doc) == "project":
            print("Resolved kind:", effective_doc.get("kind"))

        print("Dependency Graph:")
        for node, deps in graph.edges.items():
            print(node, "->", list(deps))

    _run_safely(_inner)


def cmd_apply(args):
    def _inner():
        raw_doc = load_stack_yaml(args.stack)
        effective_doc = resolve_document(raw_doc)
        plugin_names = get_plugin_names(effective_doc)
        render_context = _build_render_context(raw_doc, effective_doc)

        registry = PluginRegistry()
        registry.discover()

        _, plan = create_plan(plugin_names, registry, render_context=render_context)

        project_name = resolve_project_name(effective_doc)
        output_root = Path("output") / project_name

        print(f"\nApplying ForgeStack Plan into: {output_root}\n")
        execute_plan(plan, output_root=output_root)

    _run_safely(_inner)


def cmd_plugins(args):
    def _inner():
        registry = PluginRegistry()
        registry.discover()

        print("\nInstalled Plugins:\n")
        for name in registry.list():
            print("-", name)

    _run_safely(_inner)


def cmd_presets_list(args):
    def _inner():
        stack_dir = Path("presets") / "stack"
        app_dir = Path("presets") / "app"

        stacks = _list_yaml_stems(stack_dir)
        apps = _list_yaml_stems(app_dir)

        print("\nStack Presets:\n")
        for name in stacks:
            print("-", name)

        print("\nApp Presets:\n")
        for name in apps:
            print("-", name)

    _run_safely(_inner)


def cmd_create_project(args):
    def _inner():
        project_doc = {
            "kind": "project",
            "name": args.name,
            "uses": {
                "stack": args.stack,
                "app": args.app,
            },
            "overrides": {},
        }

        projects_dir = Path("projects")
        projects_dir.mkdir(parents=True, exist_ok=True)

        output_path = projects_dir / f"{args.name}.yaml"
        if output_path.exists() and not args.force:
            raise RuntimeError(
                f"Project file already exists: {output_path} (use --force to overwrite)"
            )

        with output_path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(project_doc, f, sort_keys=False)

        print(f"Created project file: {output_path}")

    _run_safely(_inner)


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

    presets_cmd = sub.add_parser("presets")
    presets_sub = presets_cmd.add_subparsers(dest="presets_command")

    presets_list_cmd = presets_sub.add_parser("list")
    presets_list_cmd.set_defaults(func=cmd_presets_list)

    create_cmd = sub.add_parser("create")
    create_sub = create_cmd.add_subparsers(dest="create_command")

    create_project_cmd = create_sub.add_parser("project")
    create_project_cmd.add_argument("name")
    create_project_cmd.add_argument("--stack", required=True)
    create_project_cmd.add_argument("--app", required=True)
    create_project_cmd.add_argument("--force", action="store_true")
    create_project_cmd.set_defaults(func=cmd_create_project)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)


def run_cli():
    return main()