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
            "pipelines/__init__.py",
            template="kedro/pipelines___init__.py",
        )
        ctx.plan.create_file(
            "pipelines/sample_pipeline.py",
            template="kedro/sample_pipeline.py",
        )
        ctx.plan.create_file(
            "data/README.md",
            template="kedro/data_README.md",
        )
        ctx.plan.create_file(
            "data/.gitkeep",
            template="kedro/data_gitkeep",
        )
        ctx.plan.create_file(
            "conf/README.md",
            template="kedro/conf_README.md",
        )
        ctx.plan.create_file(
            "conf/base/parameters.yml",
            template="kedro/conf_base_parameters.yml",
        )
        ctx.plan.create_file(
            "conf/local/README.md",
            template="kedro/conf_local_README.md",
        )


plugin = KedroPlugin()