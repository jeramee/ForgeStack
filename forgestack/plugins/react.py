from forgestack.core.plugin_api import Plugin


class ReactPlugin(Plugin):

    def __init__(self):
        super().__init__("react")

    def plan(self, ctx):

        ctx.plan.create_file(
            "frontend/package.json",
            template="react_package"
        )


plugin = ReactPlugin()