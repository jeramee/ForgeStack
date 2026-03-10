from pathlib import Path
import yaml


class PluginContext:
    """
    Simple runtime context for ad-hoc file mutation workflows.

    This file is preserved for backward compatibility with earlier direct-write
    plugins and manual tests. The composition-platform path uses
    forgestack.core.plugin_api.PluginContext instead.
    """

    def __init__(self, cfg, root, interactive: bool = True):
        self.cfg = cfg
        self.root = Path(root)
        self.interactive = interactive
        self.required_plugins = []
        self.capabilities: set[str] = set()
        self.env: dict[str, str] = {}

    def require(self, plugin):
        if plugin not in self.required_plugins:
            self.required_plugins.append(plugin)

    def append_file(self, path, text):
        f = self.root / path
        f.parent.mkdir(parents=True, exist_ok=True)

        existing = ""
        if f.exists():
            existing = f.read_text(encoding="utf-8")

        if text not in existing:
            f.write_text(existing + text, encoding="utf-8")

    def write_file(self, path, text):
        f = self.root / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")

    def patch_yaml(self, path, patch):
        f = self.root / path
        data = {}
        if f.exists():
            data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}

        def merge(a, b):
            for k, v in b.items():
                if isinstance(v, dict) and isinstance(a.get(k), dict):
                    merge(a[k], v)
                else:
                    a[k] = v

        merge(data, patch)
        f.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
