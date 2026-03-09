from devscaffold.core.plugin_api import Plugin, PluginMetadata


class CeleryPlugin(Plugin):
    metadata = PluginMetadata(
        name="celery",
        version="1.0.0",
        requires=["redis", "fastapi"],
        provides=["worker"],
        description="Add Celery worker support",
        compatible_core=">=0.1.0",
    )

    def plan(self, ctx):
        ctx.create_dir("backend/app", "Ensure backend app directory exists")
        ctx.create_file("backend/app/worker.py", "from celery import Celery\n\ncelery_app = Celery(\n    \"worker\",\n    broker=\"redis://redis:6379/0\",\n    backend=\"redis://redis:6379/0\",\n)\n", "Create Celery worker module")
        ctx.add_service("worker", {"build": "./backend", "volumes": ["./backend:/app"], "command": ["celery", "-A", "app.worker.celery_app", "worker", "--loglevel=info"], "depends_on": ["redis", "backend"]}, "Add Celery worker service")
        ctx.append_file("backend/requirements.txt", "celery\nredis\n", "Append Celery requirements")


def plugin():
    return CeleryPlugin()
