from devscaffold.core.plan import Plan


class RedisPlugin:

    name = "redis"

    def plan(self, ctx):

        p = Plan()

        p.compose = {
            "services": {
                "redis": {
                    "image": "redis:7",
                    "ports": ["6379:6379"]
                }
            }
        }

        return p


def plugin():
    return RedisPlugin()