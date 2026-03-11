from forgestack.core.plugin_api import Plugin


class PythonPlugin(Plugin):

    def __init__(self):
        super().__init__("python")

    def plan(self, ctx):

        ctx.plan.create_file(
            "backend/requirements.txt",
            template="python/requirements.txt"
        )
        ctx.plan.create_file(
            "backend/Dockerfile",
            template="python/Dockerfile"
        )
        ctx.plan.create_file(
            ".gitignore",
            template="root/gitignore"
        )
        ctx.plan.create_file(
            ".env.example",
            template="root/env.example"
        )
        ctx.plan.create_file(
            "README.md",
            template="root/README.md"
        )
        ctx.plan.create_file(
            "docker-compose.yml",
            template="root/docker-compose.yml"
        )


plugin = PythonPlugin()