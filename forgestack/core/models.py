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


@dataclass(slots=True)
class ServiceSpec:
    name: str
    kind: str
    image: str | None = None
    build_context: str | None = None
    command: list[str] = field(default_factory=list)
    ports: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)
    volumes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class PackageSpec:
    manager: str
    path: str
    dependencies: list[str] = field(default_factory=list)
    dev_dependencies: list[str] = field(default_factory=list)


@dataclass(slots=True)
class FileSpec:
    path: str
    content: str
    mode: str = "replace"
    owner: str | None = None


@dataclass(slots=True)
class TaskSpec:
    name: str
    command: list[str]
    cwd: str | None = None


@dataclass(slots=True)
class PluginContribution:
    plugin_name: str
    provides: set[str] = field(default_factory=set)
    requires: set[str] = field(default_factory=set)
    services: dict[str, ServiceSpec] = field(default_factory=dict)
    packages: list[PackageSpec] = field(default_factory=list)
    files: list[FileSpec] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    tasks: dict[str, TaskSpec] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class StackModel:
    name: str
    requested_plugins: list[str] = field(default_factory=list)
    resolved_plugins: list[str] = field(default_factory=list)
    capabilities: set[str] = field(default_factory=set)
    services: dict[str, ServiceSpec] = field(default_factory=dict)
    packages: list[PackageSpec] = field(default_factory=list)
    files: list[FileSpec] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    tasks: dict[str, TaskSpec] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def summary(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "requested_plugins": list(self.requested_plugins),
            "resolved_plugins": list(self.resolved_plugins),
            "capabilities": sorted(self.capabilities),
            "services": sorted(self.services.keys()),
            "files": [file.path for file in self.files],
            "env": dict(self.env),
            "tasks": sorted(self.tasks.keys()),
            "warnings": list(self.warnings),
        }
