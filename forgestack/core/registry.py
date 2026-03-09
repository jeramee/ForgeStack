# forgestack/core/registry.py

from __future__ import annotations

import importlib
import pkgutil
from importlib.metadata import entry_points

from .plugin_api import Plugin


PLUGIN_GROUP = "forgestack.plugins"


class RegistryManager:
    """
    Unified plugin registry.

    Supports two plugin sources:

    1) Local development plugins
       forgestack/plugins/*.py

    2) Installed plugins via Python entry points
       [project.entry-points."forgestack.plugins"]
    """

    def __init__(self):
        self._plugins: dict[str, Plugin] = {}

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(self, plugin: Plugin):
        name = getattr(plugin, "name", None) or getattr(plugin, "metadata", None)

        if hasattr(plugin, "metadata"):
            name = plugin.metadata.name
        elif hasattr(plugin, "name"):
            name = plugin.name
        else:
            raise RuntimeError("Plugin must define 'name' or 'metadata.name'")

        self._plugins[name] = plugin

    # ---------------------------------------------------------
    # Access
    # ---------------------------------------------------------

    def get(self, name: str) -> Plugin:
        if name not in self._plugins:
            raise RuntimeError(f"Plugin '{name}' not installed")
        return self._plugins[name]

    def exists(self, name: str) -> bool:
        return name in self._plugins

    def list(self):
        return sorted(self._plugins.keys())

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    def discover(self):
        """
        Discover plugins from both sources.
        """

        self._discover_local_plugins()
        self._discover_entrypoint_plugins()

    # ---------------------------------------------------------
    # Local Plugins
    # ---------------------------------------------------------

    def _discover_local_plugins(self):

        try:
            package = importlib.import_module("forgestack.plugins")
        except ModuleNotFoundError:
            return

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

    # ---------------------------------------------------------
    # Entry Point Plugins
    # ---------------------------------------------------------

    def _discover_entrypoint_plugins(self):

        try:
            eps = entry_points(group=PLUGIN_GROUP)
        except TypeError:
            # compatibility with older python
            eps = entry_points().get(PLUGIN_GROUP, [])

        for ep in eps:

            try:
                obj = ep.load()
                plugin = obj() if callable(obj) else obj
                self.register(plugin)
            except Exception:
                # entrypoint plugin failed to load
                continue


# ---------------------------------------------------------
# Convenience Helpers
# ---------------------------------------------------------


def load_plugins(names: list[str]) -> list[Plugin]:
    registry = RegistryManager()
    registry.discover()
    return [registry.get(n) for n in names]


def list_available_plugins() -> list[str]:
    registry = RegistryManager()
    registry.discover()
    return registry.list()