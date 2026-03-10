import argparse

from forgestack.core.registry import PluginRegistry
from forgestack.core.planner import create_plan
from forgestack.core.stack_loader import load_stack_yaml
from forgestack.core.plan_executor import execute_plan


def cmd_plan(args):

    stack_plugins = load_stack_yaml(args.stack)

    registry = PluginRegistry()
    registry.auto_discover()

    graph, plan = create_plan(stack_plugins, registry)

    print("\nRequested:", stack_plugins)
    print("Resolved:", sorted(graph.nodes.keys()))

    print("\nExecution Plan:")

    for action in plan.actions:
        print("-", action)


def cmd_graph(args):

    stack_plugins = load_stack_yaml(args.stack)

    registry = PluginRegistry()
    registry.auto_discover()

    graph, _ = create_plan(stack_plugins, registry)

    print("\nDependency Graph:")

    for node, deps in graph.edges.items():
        print(node, "->", list(deps))

def cmd_apply(args):

    stack_plugins = load_stack(args.stack)

    registry = build_registry()

    graph, plan = create_plan(stack_plugins, registry)

    print("\nApplying ForgeStack Plan\n")

    execute_plan(plan)

def main():

    parser = argparse.ArgumentParser(prog="forgestack")

    sub = parser.add_subparsers(dest="command")

    plan_cmd = sub.add_parser("plan")
    plan_cmd.add_argument("stack")
    plan_cmd.set_defaults(func=cmd_plan)

    graph_cmd = sub.add_parser("graph")
    graph_cmd.add_argument("stack")
    graph_cmd.set_defaults(func=cmd_graph)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)

def run_cli():
    return main() 