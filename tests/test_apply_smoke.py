from pathlib import Path

import yaml

from forgestack.core.preset_resolver import resolve_project_document


def _write_yaml(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_resolved_project_contains_expected_values(tmp_path):
    _write_yaml(
        tmp_path / "presets" / "stack" / "web-stack.yaml",
        {
            "kind": "stack",
            "name": "web-stack",
            "plugins": ["python", "postgres"],
            "defaults": {
                "postgres": {
                    "port": 5432,
                    "db": "default_db",
                }
            },
        },
    )

    _write_yaml(
        tmp_path / "presets" / "app" / "finance-dashboard.yaml",
        {
            "kind": "app",
            "name": "finance-dashboard",
            "features": ["charts"],
            "defaults": {},
            "ui": {},
        },
    )

    project_doc = {
        "kind": "project",
        "name": "MyApp",
        "uses": {
            "stack": "web-stack",
            "app": "finance-dashboard",
        },
        "overrides": {
            "postgres": {
                "db": "finance_app",
            }
        },
    }

    resolved = resolve_project_document(project_doc, base_dir=tmp_path)

    assert resolved["name"] == "MyApp"
    assert resolved["values"]["postgres"]["db"] == "finance_app"
    assert "python" in resolved["plugins"]
    assert "postgres" in resolved["plugins"]