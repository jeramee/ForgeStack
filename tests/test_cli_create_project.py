from pathlib import Path
import argparse
import yaml

from forgestack.cli.main import cmd_create_project


def test_create_project_writes_expected_yaml(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    args = argparse.Namespace(
        name="MyApp",
        stack="web-stack",
        app="finance-dashboard",
        force=False,
    )

    cmd_create_project(args)

    project_file = tmp_path / "projects" / "MyApp.yaml"
    assert project_file.exists()

    doc = yaml.safe_load(project_file.read_text(encoding="utf-8"))
    assert doc == {
        "kind": "project",
        "name": "MyApp",
        "uses": {
            "stack": "web-stack",
            "app": "finance-dashboard",
        },
        "overrides": {},
    }