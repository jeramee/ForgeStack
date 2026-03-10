import pytest

from forgestack.config.validators import (
    ValidationError,
    validate_and_normalize_document,
)


def test_app_features_mapping_is_valid():
    doc = {
        "kind": "app",
        "name": "finance-dashboard",
        "features": {
            "charts": True,
            "auth": True,
        },
        "defaults": {},
        "ui": {},
    }

    normalized = validate_and_normalize_document(doc, "app")

    assert normalized["kind"] == "app"
    assert normalized["features"] == {
        "charts": True,
        "auth": True,
    }


def test_app_features_list_is_normalized_to_mapping():
    doc = {
        "kind": "app",
        "name": "finance-dashboard",
        "features": ["charts", "auth", "reporting"],
        "defaults": {},
        "ui": {},
    }

    normalized = validate_and_normalize_document(doc, "app")

    assert normalized["features"] == {
        "charts": True,
        "auth": True,
        "reporting": True,
    }


def test_app_features_invalid_type_fails():
    doc = {
        "kind": "app",
        "name": "finance-dashboard",
        "features": 123,
    }

    with pytest.raises(ValidationError, match="app.features"):
        validate_and_normalize_document(doc, "app")


def test_project_requires_uses_stack():
    doc = {
        "kind": "project",
        "name": "MyApp",
        "uses": {
            "app": "finance-dashboard",
        },
    }

    with pytest.raises(ValidationError, match="project.uses.stack"):
        validate_and_normalize_document(doc, "project")


def test_project_requires_uses_app():
    doc = {
        "kind": "project",
        "name": "MyApp",
        "uses": {
            "stack": "web-stack",
        },
    }

    with pytest.raises(ValidationError, match="project.uses.app"):
        validate_and_normalize_document(doc, "project")


def test_stack_plugins_must_be_a_list():
    doc = {
        "kind": "stack",
        "name": "web-stack",
        "plugins": "react",
    }

    with pytest.raises(ValidationError, match="stack.plugins"):
        validate_and_normalize_document(doc, "stack")


def test_stack_defaults_must_be_a_mapping():
    doc = {
        "kind": "stack",
        "name": "web-stack",
        "plugins": ["react"],
        "defaults": 123,
    }

    with pytest.raises(ValidationError, match="stack.defaults"):
        validate_and_normalize_document(doc, "stack")

def test_app_stack_alias_normalizes_to_default_stack():
    doc = {
        "kind": "app",
        "name": "finance-dashboard",
        "stack": "web-stack",
        "features": ["charts"],
        "defaults": {},
        "ui": {},
    }

    normalized = validate_and_normalize_document(doc, "app")

    assert normalized["default_stack"] == "web-stack"
    assert "stack" not in normalized