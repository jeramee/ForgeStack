import pkgutil
import importlib


class RegistryManager:

    def __init__(self):
        self.plugins = {}

    def register(self, plugin):
        self.plugins[plugin.metadata.name] = plugin

    def auto_discover(self):
        """
        Automatically discover plugins inside the
        forgestack.plugins package.
        """

        package = "forgestack.plugins"

        try:
            module = importlib.import_module(package)
        except ModuleNotFoundError:
            return

        for _, name, _ in pkgutil.iter_modules(module.__path__):
            mod = importlib.import_module(f"{package}.{name}")

            if hasattr(mod, "plugin"):
                self.register(mod.plugin)