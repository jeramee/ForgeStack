from devscaffold.core.plugin_api import Plugin, PluginMetadata


class FastAPIPlugin(Plugin):
    metadata = PluginMetadata(
        name="fastapi",
        version="1.0.0",
        requires=[],
        provides=["backend"],
        description="Generate a FastAPI backend service",
        compatible_core=">=0.1.0",
    )

    def plan(self, ctx):
        ctx.create_dir("backend/app", "Create backend app directory")
        ctx.create_file(
            "backend/app/main.py",
            "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get(\"/\")\ndef root():\n    return {\"status\": \"ok\"}\n",
            "Create FastAPI entrypoint",
        )
        ctx.create_file("backend/requirements.txt", "fastapi\nuvicorn[standard]\n", "Create backend requirements")
        ctx.create_file(
            "backend/Dockerfile",
            "FROM python:3.11\n\nWORKDIR /app\n\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\n\nCOPY . .\n\nCMD [\"uvicorn\",\"app.main:app\",\"--host\",\"0.0.0.0\",\"--port\",\"8000\"]\n",
            "Create backend Dockerfile",
        )
        ctx.add_service("backend", {"build": "./backend", "volumes": ["./backend:/app"], "ports": ["8000:8000"]}, "Add backend service")


def plugin():
    return FastAPIPlugin()
