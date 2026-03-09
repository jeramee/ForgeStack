from devscaffold.core.plugin_api import Plugin, PluginMetadata


class RedisPlugin(Plugin):
    metadata = PluginMetadata(
        name="redis",
        version="1.0.0",
        requires=[],
        provides=["queue"],
        description="Add a Redis service",
        compatible_core=">=0.1.0",
    )

    def plan(self, ctx):
        ctx.add_service("redis", {"image": "redis:7", "ports": ["6379:6379"]}, "Add Redis service")


def plugin():
    return RedisPlugin()
