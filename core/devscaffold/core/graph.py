from __future__ import annotations

from dataclasses import dataclass, field

from .registry import RegistryManager


@dataclass(slots=True)
class GraphNode:
    name: str
    requires: list[str] = field(default_factory=list)


@dataclass(slots=True)
class DependencyGraph:
    nodes: dict[str, GraphNode] = field(default_factory=dict)
    edges: dict[str, set[str]] = field(default_factory=dict)


class GraphBuilder:
    def build(self, plugin_names: list[str], registry: RegistryManager) -> DependencyGraph:
        graph = DependencyGraph()
        for name in plugin_names:
            plugin = registry.load(name)
            requires = list(plugin.metadata.requires)
            graph.nodes[name] = GraphNode(name=name, requires=requires)
            graph.edges.setdefault(name, set())
            for dep in requires:
                graph.edges[name].add(dep)
        return graph


class GraphSorter:
    def topo_sort(self, graph: DependencyGraph) -> list[str]:
        visited: set[str] = set()
        temp: set[str] = set()
        order: list[str] = []

        def dfs(node: str) -> None:
            if node in temp:
                raise ValueError(f"Cycle detected at plugin '{node}'")
            if node in visited:
                return
            temp.add(node)
            for dep in sorted(graph.edges.get(node, set())):
                dfs(dep)
            temp.remove(node)
            visited.add(node)
            order.append(node)

        for node in sorted(graph.nodes):
            dfs(node)
        return order


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
