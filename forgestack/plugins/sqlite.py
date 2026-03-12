from forgestack.core.plugin_api import Plugin


class SQLitePlugin(Plugin):
    def __init__(self):
        super().__init__("sqlite", requires=["python"])

    def plan(self, ctx):
        ctx.plan.create_file(
            "backend/db.py",
            template="sqlite/db.py",
        )


plugin = SQLitePlugin()