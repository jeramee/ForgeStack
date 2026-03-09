from .resolver import build_dependency_graph
import threading


class Plan:

    def __init__(self):
        self.actions = []
        self._lock = threading.Lock()

    def add(self, action):
        with self._lock:
            self.actions.append(action)

class PluginContext:
    def __init__(self, plan):
        self.plan = plan


from .resolver import build_dependency_graph
from .dag_executor import execute_dag

from .resolver import build_dependency_graph
from .dag_executor import execute_dag


def create_plan(stack_plugins, registry):

    graph = build_dependency_graph(stack_plugins, registry)

    plan = Plan()

    def ctx_factory(plugin_name):
        return PluginContext(plan)

    execute_dag(graph, registry, ctx_factory)

    return graph, plan