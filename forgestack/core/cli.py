import argparse

from forgestack.core.registry import PluginRegistry
from forgestack.core.planner import create_plan
from forgestack.core.stack_loader import load_stack_yaml


def cmd_plugins(registry):

    print("\nInstalled Plugins:\n")

    for name in sorted(registry.plugins.keys()):
        print("-", name)

def cmd_graph(stack_file, registry):

    stack_plugins = load_stack_yaml(stack_file)

    graph, _ = create_plan(stack_plugins, registry)

    print("\nDependency Graph:\n")

    for node in sorted(graph.edges):

        deps = graph.edges[node]

        if deps:
            print(f"{node} -> {sorted(deps)}")
        else:
            print(f"{node} -> []")

def run_cli():

    parser = argparse.ArgumentParser(prog="forgestack")

    sub = parser.add_subparsers(dest="command")

    plan_cmd = sub.add_parser("plan")
    plan_cmd.add_argument("stack")

    graph_cmd = sub.add_parser("graph")
    graph_cmd.add_argument("stack")

    sub.add_parser("plugins")

    args = parser.parse_args()

    registry = PluginRegistry()
    registry.auto_discover()

    if args.command == "plan":

        stack_plugins = load_stack_yaml(args.stack)

        graph, plan = create_plan(stack_plugins, registry)

        print("\nRequested:", stack_plugins)
        print("Resolved:", sorted(graph.resolved))

        print("\nExecution Plan:\n")

        for action in plan.actions:
            print("-", action)

    elif args.command == "graph":

        cmd_graph(args.stack, registry)

    else:

        parser.print_help()