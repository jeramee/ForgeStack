from pathlib import Path

import pytest
import yaml

from forgestack.core.preset_resolver import resolve_project_document


def _write_yaml(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_resolve_project_document_merges_plugins_and_values(tmp_path):
    _write_yaml(
        tmp_path / "presets" / "stack" / "web-stack.yaml",
        {
            "kind": "stack",
            "name": "web-stack",
            "plugins": ["python", "fastapi", "postgres"],
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
            "plugins": ["react", "postgres"],
            "features": ["charts", "auth"],
            "defaults": {
                "postgres": {
                    "db": "finance_dashboard",
                },
                "branding": {
                    "theme": "finance",
                },
            },
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

    assert resolved["kind"] == "resolved-project"
    assert resolved["name"] == "MyApp"
    assert resolved["plugins"] == ["python", "fastapi", "postgres", "react"]

    assert resolved["values"]["postgres"]["port"] == 5432
    assert resolved["values"]["postgres"]["db"] == "finance_app"
    assert resolved["values"]["branding"]["theme"] == "finance"


def test_missing_stack_preset_fails(tmp_path):
    _write_yaml(
        tmp_path / "presets" / "app" / "finance-dashboard.yaml",
        {
            "kind": "app",
            "name": "finance-dashboard",
            "features": {},
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
        "overrides": {},
    }

    with pytest.raises(FileNotFoundError):
        resolve_project_document(project_doc, base_dir=tmp_path)


def test_missing_app_preset_fails(tmp_path):
    _write_yaml(
        tmp_path / "presets" / "stack" / "web-stack.yaml",
        {
            "kind": "stack",
            "name": "web-stack",
            "plugins": ["python"],
            "defaults": {},
        },
    )

    project_doc = {
        "kind": "project",
        "name": "MyApp",
        "uses": {
            "stack": "web-stack",
            "app": "finance-dashboard",
        },
        "overrides": {},
    }

    with pytest.raises(FileNotFoundError):
        resolve_project_document(project_doc, base_dir=tmp_path)

def test_local_workflow_project_resolves_sqlite_stack_and_app(tmp_path):
    _write_yaml(
        tmp_path / "presets" / "stack" / "local-workflow-stack.yaml",
        {
            "kind": "stack",
            "name": "local-workflow-stack",
            "plugins": ["react", "fastapi", "sqlite"],
            "defaults": {},
        },
    )

    _write_yaml(
        tmp_path / "presets" / "app" / "local-workflow-console.yaml",
        {
            "kind": "app",
            "name": "local-workflow-console",
            "stack": "local-workflow-stack",
            "features": {
                "queue": True,
                "intake": True,
                "review": True,
            },
            "defaults": {},
            "ui": {},
        },
    )

    project_doc = {
        "kind": "project",
        "name": "LocalWorkflowApp",
        "uses": {
            "stack": "local-workflow-stack",
            "app": "local-workflow-console",
        },
        "overrides": {
            "sqlite": {
                "database": "app.db",
            }
        },
    }

    resolved = resolve_project_document(project_doc, base_dir=tmp_path)

    assert resolved["kind"] == "resolved-project"
    assert resolved["name"] == "LocalWorkflowApp"
    assert resolved["plugins"] == ["react", "fastapi", "sqlite"]
    assert resolved["stack"]["name"] == "local-workflow-stack"
    assert resolved["app"]["name"] == "local-workflow-console"
    assert resolved["values"]["sqlite"]["database"] == "app.db"