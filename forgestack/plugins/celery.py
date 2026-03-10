from forgestack.core.plugin_api import Plugin


class CeleryPlugin(Plugin):

    def __init__(self):
        super().__init__("celery", ["python", "redis"])

    def plan(self, ctx):
        ctx.plan.create_file(
            "backend/celery_app.py",
            template="celery_app"
        )
        ctx.plan.create_file(
            "backend/tasks.py",
            template="celery_tasks"
        )
        ctx.plan.create_file(
            "docker/celery.yml",
            template="celery_docker"
        )


plugin = CeleryPlugin()