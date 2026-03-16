# Active public planner for `devmake plan` / `devmake apply`.
# Public generation behavior should be improved here in place unless there is an
# intentional migration away from this path.
import threading
from .resolver import build_dependency_graph
from .dag_executor import execute_dag


class Plan:

    def __init__(self, render_context=None):
        self.actions = []
        self._lock = threading.Lock()
        self.render_context = render_context or {}

    def add(self, action):
        with self._lock:
            self.actions.append(action)

    def create_file(self, path, template=None, content=None):
        self.add({
            "type": "create_file",
            "path": path,
            "template": template,
            "content": content,
        })


class PluginContext:

    def __init__(self, plan):
        self.plan = plan


def create_plan(stack_plugins, registry, render_context=None):
    graph = build_dependency_graph(stack_plugins, registry)

    plan = Plan(render_context=render_context)

    def ctx_factory(plugin_name):
        return PluginContext(plan)

    execute_dag(graph, registry, ctx_factory)

    return graph, plan