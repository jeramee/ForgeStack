from __future__ import annotations

from pathlib import Path
import yaml

from ..models import StackModel


class DockerComposeRenderer:
    def render(self, model: StackModel, root: str) -> None:
        compose: dict = {"services": {}}
        volumes: dict[str, dict] = {}

        for name, service in model.services.items():
            spec: dict = {}
            if service.image:
                spec["image"] = service.image
            if service.build_context:
                spec["build"] = service.build_context
            if service.command:
                spec["command"] = service.command
            if service.ports:
                spec["ports"] = service.ports
            if service.env:
                spec["environment"] = service.env
            if service.depends_on:
                spec["depends_on"] = service.depends_on
            if service.volumes:
                spec["volumes"] = service.volumes
                for vol in service.volumes:
                    if ":" in vol:
                        vol_name = vol.split(":", 1)[0]
                        if "/" not in vol_name and "\\" not in vol_name and not vol_name.startswith("."):
                            volumes[vol_name] = {}

            compose["services"][name] = spec

        if volumes:
            compose["volumes"] = volumes

        out = Path(root) / "docker-compose.yml"
        out.write_text(yaml.safe_dump(compose, sort_keys=False), encoding="utf-8")
