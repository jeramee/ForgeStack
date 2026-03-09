from devscaffold.core.plugin_api import Plugin, PluginMetadata


class AuthPlugin(Plugin):
    metadata = PluginMetadata(
        name="auth",
        version="1.0.0",
        requires=["fastapi"],
        provides=["auth"],
        description="Add a simple FastAPI auth router",
        compatible_core=">=0.1.0",
    )

    def plan(self, ctx):
        ctx.create_file("backend/app/auth.py", "from fastapi import APIRouter\n\nrouter = APIRouter()\n\n@router.get(\"/auth\")\ndef auth_status():\n    return {\"auth\": \"ready\"}\n", "Create auth router")
        ctx.append_file("backend/app/main.py", "\nfrom app.auth import router as auth_router\napp.include_router(auth_router)\n", "Register auth router")


def plugin():
    return AuthPlugin()
