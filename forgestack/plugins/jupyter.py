from forgestack.core.plugin_api import Plugin


class JupyterPlugin(Plugin):
    def __init__(self):
        super().__init__("jupyter", requires=["python"])

    def plan(self, ctx):
        ctx.plan.create_file(
            "notebooks/README.md",
            template="jupyter/README.md",
        )


plugin = JupyterPlugin()