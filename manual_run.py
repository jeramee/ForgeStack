from forgestack.core.registry import PluginRegistry
from forgestack.core.planner import create_plan

from forgestack.plugins.fastapi import FastAPIPlugin
from forgestack.plugins.redis import RedisPlugin
from forgestack.plugins.postgres import PostgresPlugin
from forgestack.plugins.python import PythonPlugin

# create registry
registry = PluginRegistry()

# register plugins
registry.register(FastAPIPlugin())
registry.register(RedisPlugin())
registry.register(PostgresPlugin())
registry.register(PythonPlugin())

# pretend stack.yaml requested these
stack_plugins = ["fastapi"]

# generate plan
graph, plan = create_plan(stack_plugins, registry)

print("Requested:", graph.requested)
print("Resolved:", graph.resolved)

print("\nDependency Graph:")
for k,v in graph.edges.items():
    print(k,"->",v)

print("\nExecution Order:")
print(graph.topo_sort())

print("\nPlan Actions:")
for a in plan.actions:
    print(a)