from devscaffold.core.plugin_api import Plugin, PluginMetadata


class PostgresPlugin(Plugin):
    metadata = PluginMetadata(
        name="postgres",
        version="1.0.0",
        requires=[],
        provides=["database"],
        description="Add a PostgreSQL database service",
        compatible_core=">=0.1.0",
    )

    def plan(self, ctx):
        ctx.add_service("db", {"image": "postgres:16", "environment": {"POSTGRES_DB": "appdb", "POSTGRES_USER": "appuser", "POSTGRES_PASSWORD": "devpass"}, "ports": ["5432:5432"], "volumes": ["pgdata:/var/lib/postgresql/data"]}, "Add Postgres service")
        ctx.add_service("volume:pgdata", {}, "Add Postgres volume")
        ctx.append_file("backend/.env", "DATABASE_URL=postgresql://appuser:devpass@db:5432/appdb\n", "Write backend database environment")


def plugin():
    return PostgresPlugin()
