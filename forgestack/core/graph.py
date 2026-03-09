# forgestack/core/graph.py

from __future__ import annotations

from dataclasses import dataclass, field

from .registry import RegistryManager


# ---------------------------------------------------------
# Graph Data Structures
# ---------------------------------------------------------

@dataclass(slots=True)
class GraphNode:
    name: str
    requires: list[str] = field(default_factory=list)


@dataclass(slots=True)
class DependencyGraph:
    nodes: dict[str, GraphNode] = field(default_factory=dict)
    edges: dict[str, set[str]] = field(default_factory=dict)


# ---------------------------------------------------------
# Graph Builder
# ---------------------------------------------------------

class GraphBuilder:
    """
    Builds a full dependency graph from requested plugins.
    Resolves transitive dependencies automatically.
    """

    def build(self, plugin_names: list[str], registry: RegistryManager) -> DependencyGraph:

        graph = DependencyGraph()

        to_process = list(plugin_names)
        processed = set()

        while to_process:

            name = to_process.pop()

            if name in processed:
                continue

            if not registry.exists(name):
                raise RuntimeError(f"Plugin '{name}' not found")

            plugin = registry.get(name)

            requires = list(getattr(plugin, "requires", []))

            graph.nodes[name] = GraphNode(name=name, requires=requires)

            graph.edges.setdefault(name, set())

            for dep in requires:
                graph.edges[name].add(dep)
                if dep not in processed:
                    to_process.append(dep)

            processed.add(name)

        return graph


# ---------------------------------------------------------
# Topological Sort
# ---------------------------------------------------------

class GraphSorter:

    def topo_sort(self, graph: DependencyGraph) -> list[str]:

        visited: set[str] = set()
        visiting: set[str] = set()
        order: list[str] = []

        def dfs(node: str):

            if node in visiting:
                cycle = " -> ".join(list(visiting) + [node])
                raise RuntimeError(f"Dependency cycle detected: {cycle}")

            if node in visited:
                return

            visiting.add(node)

            for dep in sorted(graph.edges.get(node, set())):
                dfs(dep)

            visiting.remove(node)
            visited.add(node)
            order.append(node)

        for node in sorted(graph.nodes):
            dfs(node)

        return order


# ---------------------------------------------------------
# CLI Graph Renderer
# ---------------------------------------------------------

class GraphRenderer:

    def render(self, graph: DependencyGraph, ordered_plugins: list[str]) -> str:

        lines = ["ForgeStack Dependency Graph", ""]

        for name in ordered_plugins:

            deps = sorted(graph.edges.get(name, set()))

            if deps:
                lines.append(f"- {name} -> {', '.join(deps)}")
            else:
                lines.append(f"- {name}")

        return "\n".join(lines)