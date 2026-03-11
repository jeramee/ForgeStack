from forgestack.core.plugin_api import Plugin
from forgestack.core.plugin_api import Plugin


class CeleryPlugin(Plugin):

    def __init__(self):
        super().__init__("celery", ["python", "redis"])

    def plan(self, ctx):
        ctx.plan.create_file(
            "backend/celery_app.py",
            template="celery/app.py"
        )
        ctx.plan.create_file(
            "backend/tasks.py",
            template="celery/tasks.py"
        )
        ctx.plan.create_file(
            "docker/celery.yml",
            template="docker/celery.yml"
        )


plugin = CeleryPlugin()