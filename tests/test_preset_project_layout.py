from pathlib import Path

import yaml


def _load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_project_files_are_projects():
    for path in Path("projects").glob("*.yaml"):
        doc = _load_yaml(path)
        assert doc is not None, f"{path} is empty"
        assert isinstance(doc, dict), f"{path} must load as a YAML mapping"
        assert doc.get("kind") == "project", f"{path} must have kind: project"


def test_app_presets_are_apps():
    for path in Path("presets/app").glob("*.yaml"):
        doc = _load_yaml(path)
        assert doc is not None, f"{path} is empty"
        assert isinstance(doc, dict), f"{path} must load as a YAML mapping"
        assert doc.get("kind") == "app", f"{path} must have kind: app"


def test_stack_presets_are_stacks_or_legacy():
    for path in Path("presets/stack").glob("*.yaml"):
        doc = _load_yaml(path)

        assert doc is not None, f"{path} is empty"
        assert isinstance(doc, dict), f"{path} must load as a YAML mapping"

        # Canonical stack docs should declare kind: stack.
        if doc.get("kind") == "stack":
            continue

        # Allow a narrow legacy fallback shape for older stack docs that are still valid.
        has_plugins = isinstance(doc.get("plugins"), list)
        if has_plugins:
            continue

        raise AssertionError(
            f"{path} must be a stack document with kind: stack or a valid legacy stack shape"
        )