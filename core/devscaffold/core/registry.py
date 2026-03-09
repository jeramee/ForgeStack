from __future__ import annotations

from importlib.metadata import entry_points

from packaging.specifiers import SpecifierSet
from packaging.version import Version

from devscaffold import __version__
from .plugin_api import PluginMetadata

PLUGIN_GROUPS = ("forgestack.plugins", "devscaffold.plugins")


class RegistryManager:
    def __init__(self, groups: tuple[str, ...] = PLUGIN_GROUPS) -> None:
        self.groups = groups
        self._cache = None

    @classmethod
    def default(cls) -> "RegistryManager":
        return cls()

    def _entry_points(self):
        if self._cache is not None:
            return self._cache
        discovered = {}
        for group in self.groups:
            for ep in entry_points(group=group):
                discovered.setdefault(ep.name, ep)
        self._cache = discovered
        return discovered

    def discover(self):
        metadata = []
        for name in sorted(self._entry_points()):
            try:
                plugin = self.load(name)
            except Exception:
                continue
            metadata.append(plugin.metadata)
        return metadata

    def exists(self, name: str) -> bool:
        return name in self._entry_points()

    def load(self, name: str):
        eps = self._entry_points()
        if name not in eps:
            raise RuntimeError(f"Missing plugin: {name}. Installed: {sorted(eps.keys())}")
        obj = eps[name].load()
        plugin = obj() if callable(obj) else obj
        metadata = getattr(plugin, "metadata", None)
        if metadata is None:
            requires = list(getattr(plugin, "requires", []))
            plugin.metadata = PluginMetadata(name=name, requires=requires)
            metadata = plugin.metadata
        self._validate_metadata(metadata)
        return plugin

    def _validate_metadata(self, metadata: PluginMetadata) -> None:
        if not metadata.name:
            raise RuntimeError("Plugin metadata must include a name")
        spec = SpecifierSet(metadata.compatible_core or ">=0.0.0")
        if Version(__version__) not in spec:
            raise RuntimeError(f"Plugin '{metadata.name}' is not compatible with ForgeStack core {__version__}; requires {metadata.compatible_core}")


def load_plugins(names):
    registry = RegistryManager.default()
    return [registry.load(name) for name in names]


def list_available_plugins():
    return [meta.name for meta in RegistryManager.default().discover()]
