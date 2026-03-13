from forgestack.core.plugin_api import Plugin


class KedroPlugin(Plugin):
    def __init__(self):
        super().__init__("kedro", requires=["python"])

    def plan(self, ctx):
        ctx.plan.create_file(
            "pipelines/README.md",
            template="kedro/pipelines_README.md",
        )
        ctx.plan.create_file(
            "data/README.md",
            template="kedro/data_README.md",
        )
        ctx.plan.create_file(
            "conf/README.md",
            template="kedro/conf_README.md",
        )


plugin = KedroPlugin()
