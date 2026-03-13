from forgestack.core.plugin_api import Plugin


class VoilaPlugin(Plugin):
    def __init__(self):
        super().__init__("voila", requires=["python", "jupyter"])

    def plan(self, ctx):
        ctx.plan.create_file(
            "notebooks/voila_demo.ipynb",
            template="voila/voila_demo.ipynb",
        )


plugin = VoilaPlugin()
