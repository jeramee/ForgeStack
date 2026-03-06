from devscaffold.core.plan import Plan, FileWrite


class CeleryPlugin:

    name = "celery"
    requires = ["redis"]

    def plan(self, ctx):

        p = Plan()

        p.folders.append("backend/app")

        p.files.append(
            FileWrite(
                "backend/app/worker.py",
                """
from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)
"""
            )
        )

        p.compose = {
            "services": {
                "worker": {
                    "build": "./backend",
                    "volumes": ["./backend:/app"],
                    "command": [
                        "celery",
                        "-A",
                        "app.worker.celery_app",
                        "worker",
                        "--loglevel=info"
                    ],
                    "depends_on": ["redis", "backend"]
                }
            }
        }

        return p

    def after_generate(self, ctx):
        ctx.append_file("backend/requirements.txt", "celery\nredis\n")


def plugin():
    return CeleryPlugin()