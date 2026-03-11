from forgestack.core.plugin_api import Plugin


class ReactPlugin(Plugin):

    def __init__(self):
        super().__init__("react")

    def plan(self, ctx):

        ctx.plan.create_file(
            "frontend/package.json",
            template="react/package.json"
        )
        ctx.plan.create_file(
            "frontend/index.html",
            template="react/index.html"
        )
        ctx.plan.create_file(
            "frontend/src/main.jsx",
            template="react/src/main.jsx"
        )
        ctx.plan.create_file(
            "frontend/src/App.jsx",
            template="react/src/App.jsx"
        )
        ctx.plan.create_file(
            "frontend/Dockerfile",
            template="react/Dockerfile"
        )


plugin = ReactPlugin()