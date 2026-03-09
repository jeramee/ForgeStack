from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import PluginConfig, StackConfig


LEGACY_PROJECT_KEYS = {"project", "plugins"}


def _normalize_plugins(raw_plugins: list[Any], raw: dict[str, Any]) -> list[PluginConfig]:
    plugins: list[PluginConfig] = []
    for item in raw_plugins:
        if isinstance(item, str):
            plugins.append(PluginConfig(name=item, options=raw.get(item, {}) or {}))
        elif isinstance(item, dict):
            name = item.get("name")
            if not name:
                raise ValueError("Plugin objects must include a 'name' field")
            opts = dict(item.get("options", {}))
            merged_opts = {**(raw.get(name, {}) or {}), **opts}
            plugins.append(PluginConfig(name=name, enabled=item.get("enabled", True), options=merged_opts))
        else:
            raise ValueError(f"Unsupported plugin declaration: {item!r}")
    return plugins


def load_config(path: str | Path) -> StackConfig:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Stack config not found: {config_path}")

    raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}

    if "name" in raw and "plugins" in raw:
        name = raw["name"]
        raw_plugins = raw.get("plugins", [])
        options = {k: v for k, v in raw.items() if k not in {"name", "plugins"}}
    else:
        project = raw.get("project", {}) or {}
        name = project.get("name")
        raw_plugins = raw.get("plugins", [])
        options = {k: v for k, v in raw.items() if k not in LEGACY_PROJECT_KEYS}

    if not name:
        raise ValueError("Stack config must include a project name")

    plugins = _normalize_plugins(raw_plugins, raw)
    return StackConfig(name=name, plugins=plugins, options=options, raw=raw)
