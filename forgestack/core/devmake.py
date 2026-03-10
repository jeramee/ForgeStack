import argparse
from pathlib import Path

from forgestack.core.composer import StackComposer
from forgestack.core.config import load_config
from forgestack.core.executor import DefaultExecutor
from forgestack.core.graph import GraphBuilder, GraphRenderer, GraphSorter
from forgestack.core.registry import RegistryManager
from forgestack.core.validation import ConfigValidator, GraphValidator, validate_stack_errors


def _load_and_validate_config(config_path: str):
    stack = load_config(config_path)
    errors = ConfigValidator().validate(stack)
    if errors:
        raise SystemExit("\n".join(errors))
    return stack


def run_cli():
    parser = argparse.ArgumentParser(prog="devmake")
    sub = parser.add_subparsers(dest="command")

    plan_cmd = sub.add_parser("plan")
    plan_cmd.add_argument("stack")

    graph_cmd = sub.add_parser("graph")
    graph_cmd.add_argument("stack")

    apply_cmd = sub.add_parser("apply")
    apply_cmd.add_argument("stack")
    apply_cmd.add_argument("--yes", action="store_true", help="Run in non-interactive mode")

    sub.add_parser("plugins")

    args = parser.parse_args()

    registry = RegistryManager()
    registry.discover()

    if args.command == "plugins":
        print("\nInstalled Plugins:\n")
        for name in registry.list():
            print("-", name)
        return

    if args.command in {"plan", "graph", "apply"}:
        stack = _load_and_validate_config(args.stack)
        builder = GraphBuilder()
        sorter = GraphSorter()
        graph = builder.build(stack.plugin_names(), registry)
        graph_errors = GraphValidator().validate(graph, registry)
        if graph_errors:
            raise SystemExit("\n".join(graph_errors))
        ordered = sorter.topo_sort(graph)

        if args.command == "graph":
            print(GraphRenderer().render(graph, ordered))
            return

        composer = StackComposer()
        model = composer.compose(stack, ordered, registry, interactive=not getattr(args, "yes", False))
        stack_errors = validate_stack_errors(model)
        if stack_errors:
            raise SystemExit("\n".join(stack_errors))

        if args.command == "plan":
            summary = model.summary()
            print(f"Stack: {summary['name']}")
            print("\nCapabilities:")
            for item in summary["capabilities"]:
                print("-", item)
            print("\nServices:")
            for item in summary["services"]:
                print("-", item)
            print("\nFiles:")
            for item in summary["files"]:
                print("-", item)
            print("\nEnv:")
            for key, value in summary["env"].items():
                print(f"- {key}={value}")
            print("\nTasks:")
            for item in summary["tasks"]:
                print("-", item)
            return

        if args.command == "apply":
            result = DefaultExecutor().apply_model(model, Path(stack.name))
            print(f"Generated stack at: {stack.name}")
            print(f"Wrote {len(result.written_files)} files")
            return

    parser.print_help()
