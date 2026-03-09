from forgestack.core.plugin_api import Plugin


class PythonPlugin(Plugin):

    def __init__(self):
        super().__init__("python")

    def plan(self, ctx):
        ctx.plan.create_file(
            "backend/requirements.txt",
            template="python_requirements"
        )