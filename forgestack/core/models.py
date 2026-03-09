from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PluginConfig:
    name: str
    enabled: bool = True
    options: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class StackConfig:
    name: str
    plugins: list[PluginConfig]
    options: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    def plugin_names(self) -> list[str]:
        return [plugin.name for plugin in self.plugins if plugin.enabled]
