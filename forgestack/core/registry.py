import importlib
import pkgutil
from forgestack.core.plugin_api import Plugin


class PluginRegistry:

    def __init__(self):
        self.plugins = {}

    def register(self, plugin):
        print("Registered plugin:", plugin.name)
        self.plugins[plugin.name] = plugin

    def get(self, name):
        if name not in self.plugins:
            raise ValueError(f"Plugin '{name}' not installed")
        return self.plugins[name]

    def auto_discover(self):
        """
        Automatically discover plugins inside forgestack/plugins
        """

        package = importlib.import_module("forgestack.plugins")

        for _, module_name, _ in pkgutil.iter_modules(package.__path__):

            module = importlib.import_module(f"forgestack.plugins.{module_name}")

            for attr in dir(module):

                obj = getattr(module, attr)

                if (
                    isinstance(obj, type)
                    and issubclass(obj, Plugin)
                    and obj is not Plugin
                ):
                    plugin = obj()
                    self.register(plugin)