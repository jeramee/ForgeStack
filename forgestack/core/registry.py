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
    1) Local development plugins in forgestack/plugins
    2) Installed plugins via Python entry points
    """

    def __init__(self):
        self._plugins: dict[str, Plugin] = {}
        self._discovered = False

    def register(self, plugin: Plugin):
        name = getattr(plugin, "name", None) or getattr(plugin, "metadata", None)
        if hasattr(plugin, "metadata"):
            name = plugin.metadata.name
        elif hasattr(plugin, "name"):
            name = plugin.name
        else:
            raise RuntimeError("Plugin must define 'name' or 'metadata.name'")
        self._plugins[name] = plugin

    def ensure_discovered(self) -> None:
        if not self._discovered:
            self.discover()

    def get(self, name: str) -> Plugin:
        self.ensure_discovered()
        if name not in self._plugins:
            raise RuntimeError(f"Plugin '{name}' not installed")
        return self._plugins[name]

    def load(self, name: str) -> Plugin:
        return self.get(name)

    def exists(self, name: str) -> bool:
        self.ensure_discovered()
        return name in self._plugins

    def list(self):
        self.ensure_discovered()
        return sorted(self._plugins.keys())

    def discover(self):
        self._plugins = {}
        self._discover_local_plugins()
        self._discover_entrypoint_plugins()
        self._discovered = True

    def _discover_local_plugins(self):
        try:
            package = importlib.import_module("forgestack.plugins")
        except ModuleNotFoundError:
            return

        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            try:
                module = importlib.import_module(f"forgestack.plugins.{module_name}")
            except Exception:
                continue

            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, type) and issubclass(obj, Plugin) and obj is not Plugin:
                    try:
                        plugin = obj()
                        self.register(plugin)
                    except Exception:
                        continue

    def _discover_entrypoint_plugins(self):
        try:
            eps = entry_points(group=PLUGIN_GROUP)
        except TypeError:
            eps = entry_points().get(PLUGIN_GROUP, [])

        for ep in eps:
            try:
                obj = ep.load()
                plugin = obj() if callable(obj) else obj
                self.register(plugin)
            except Exception:
                continue

    def auto_discover(self):
        """
        Discover plugins inside forgestack.plugins
        """

        package = importlib.import_module("forgestack.plugins")

        for _, module_name, _ in pkgutil.iter_modules(package.__path__):

            module = importlib.import_module(
                f"forgestack.plugins.{module_name}"
            )

            if hasattr(module, "plugin"):
                self.register(module.plugin)
# Backward-compatible alias for older code
PluginRegistry = RegistryManager


def load_plugins(names: list[str]) -> list[Plugin]:
    registry = RegistryManager()
    registry.discover()
    return [registry.get(n) for n in names]


def list_available_plugins() -> list[str]:
    registry = RegistryManager()
    registry.discover()
    return registry.list()

