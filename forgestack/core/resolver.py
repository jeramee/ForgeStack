from .graph import DependencyGraph, GraphNode


def build_dependency_graph(stack_plugins, registry):

    resolved = set()
    edges = {}
    nodes = {}

    def visit(name):

        if name in resolved:
            return

        plugin = registry.get(name)

        deps = list(getattr(plugin, "requires", []))

        nodes[name] = GraphNode(name=name, requires=deps)
        edges[name] = set(deps)

        for dep in deps:
            visit(dep)

        resolved.add(name)

    for name in stack_plugins:
        visit(name)

    graph = DependencyGraph(nodes=nodes, edges=edges)

    return graph