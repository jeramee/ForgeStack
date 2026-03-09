from forgestack.core.plugin_api import Plugin


class PostgresPlugin(Plugin):

    def __init__(self):
        super().__init__("postgres")

    def plan(self, ctx):
        ctx.plan.create_file(
            "docker/postgres.yml",
            template="postgres_docker"
        )