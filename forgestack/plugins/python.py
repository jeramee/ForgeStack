from forgestack.core.plugin_api import Plugin
from forgestack.core.models import PluginContribution


class PythonPlugin(Plugin):

    def __init__(self):
        super().__init__("python")

    # NEW composition-style contribution
    def contribute(self, ctx):

        return PluginContribution(
            plugin_name=self.name,
            provides={"runtime:python"},
        )

    # OLD scaffolding behaviour (still supported)
    def plan(self, ctx):
        ctx.plan.create_file(
            "backend/requirements.txt",
            template="python_requirements"
        )