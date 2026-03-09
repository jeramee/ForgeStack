from forgestack.core.plugin_api import Plugin

class RedisPlugin(Plugin):
    def __init__(self):
        super().__init__("redis")

    def plan(self, ctx):
        ctx.plan.create_file(
            "docker/redis.yml",
            template="redis_docker"
        )