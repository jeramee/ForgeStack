from .graph import DependencyGraph

def build_dependency_graph(stack_plugins, registry):

    resolved = set()
    edges = {}

    def visit(name):

        if name in resolved:
            return

        plugin = registry.get(name)

        deps = plugin.requires
        edges[name] = set(deps)

        for dep in deps:
            visit(dep)

        resolved.add(name)

    for name in stack_plugins:
        visit(name)

    graph = DependencyGraph(edges, set(stack_plugins), resolved)

    return graph