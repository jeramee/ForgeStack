class FastAPIPlugin(Plugin):

    def __init__(self):
        super().__init__("fastapi", ["python"])

    def plan(self, ctx):

        ctx.plan.create_directory("backend")

        ctx.plan.create_file(
            "backend/main.py",
            template="fastapi_main"
        )