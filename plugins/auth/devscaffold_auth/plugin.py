from devscaffold.core.plan import Plan, FileWrite


class AuthPlugin:

    name = "auth"
    requires = ["fastapi"]

    def plan(self, ctx):

        p = Plan()

        p.files.append(
            FileWrite(
                "backend/app/auth.py",
                """
from fastapi import APIRouter

router = APIRouter()

@router.get("/auth")
def auth_status():
    return {"auth": "ready"}
"""
            )
        )

        return p

def after_generate(self, ctx):

    ctx.append_file(
        "backend/app/main.py",
        "\nfrom app.auth import router as auth_router\napp.include_router(auth_router)\n"
    )

def plugin():
    return AuthPlugin()