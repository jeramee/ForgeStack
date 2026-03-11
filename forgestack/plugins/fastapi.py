from forgestack.core.plugin_api import Plugin


class FastAPIPlugin(Plugin):

    def __init__(self):
        super().__init__("fastapi", requires=["python"])

    def plan(self, ctx):

        ctx.plan.create_file(
            "backend/main.py",
            template="fastapi/main.py"
        )
        ctx.plan.create_file(
            "backend/app_config.py",
            template="fastapi/app_config.py"
        )


plugin = FastAPIPlugin()