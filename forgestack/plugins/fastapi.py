from forgestack.core.plugin_api import Plugin
from forgestack.core.context import PluginContext


class FastAPIPlugin(Plugin):

    def __init__(self):
        super().__init__("fastapi", ["python"])

    def plan(self, ctx: PluginContext):

        ctx.append_file(
            "backend/main.py",
            """
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}
"""
        )