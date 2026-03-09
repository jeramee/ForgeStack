from pathlib import Path
from .plugin_api import PluginContext

import yaml


class Context:

    def __init__(self, cfg, root):

        self.cfg = cfg
        self.root = Path(root)
        self.required_plugins = []

    def require(self, plugin):

        if plugin not in self.required_plugins:
            self.required_plugins.append(plugin)

    def append_file(self, path, text):

        f = self.root / path
        f.parent.mkdir(parents=True, exist_ok=True)

        existing = ""
        if f.exists():
            existing = f.read_text()

        if text not in existing:
            f.write_text(existing + text)

    def patch_yaml(self, path, patch):

        f = self.root / path

        data = {}

        if f.exists():
            data = yaml.safe_load(f.read_text()) or {}

        def merge(a, b):

            for k, v in b.items():

                if isinstance(v, dict) and isinstance(a.get(k), dict):
                    merge(a[k], v)
                else:
                    a[k] = v

        merge(data, patch)

        f.write_text(yaml.safe_dump(data, sort_keys=False))