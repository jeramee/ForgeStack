from dataclasses import dataclass, field

@dataclass
class DependencyGraph:
    edges: dict[str, set[str]] = field(default_factory=dict)
    requested: set[str] = field(default_factory=set)
    resolved: set[str] = field(default_factory=set)

    def add_node(self, name: str):
        self.edges.setdefault(name, set())
        self.resolved.add(name)

    def add_edge(self, plugin: str, dependency: str):
        self.add_node(plugin)
        self.add_node(dependency)
        self.edges[plugin].add(dependency)

    def topo_sort(self):
        visited = set()
        visiting = set()
        order = []

        def dfs(node):
            if node in visiting:
                cycle = " -> ".join(list(visiting) + [node])
                raise ValueError(f"Dependency cycle detected: {cycle}")

            if node in visited:
                return

            visiting.add(node)

            for dep in sorted(self.edges.get(node, [])):
                dfs(dep)

            visiting.remove(node)
            visited.add(node)
            order.append(node)

        for node in sorted(self.resolved):
            dfs(node)

        return order