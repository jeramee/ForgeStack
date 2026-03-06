from devscaffold.core.plan import Plan, Command


class ReactPlugin:

    name = "react"

    def plan(self, ctx):

        port = ctx.cfg.get("react", {}).get("port", 5173)

        p = Plan()

        p.folders.append("frontend")

        p.commands.append(
            Command(["npm", "create", "vite@latest", "frontend", "--", "--template", "react"])
        )

        p.compose = {
            "services": {
                "frontend": {
                    "image": "node:20",
                    "working_dir": "/app",
                    "volumes": ["./frontend:/app"],
                    "ports": [f"{port}:{port}"],
                    "command": ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
                }
            }
        }

        return p


def plugin():
    return ReactPlugin()