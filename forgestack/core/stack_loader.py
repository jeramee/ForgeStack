from pathlib import Path
import yaml

from forgestack.config.validators import (
    ValidationError,
    validate_and_normalize_document,
)


def load_stack_yaml(path):
    """
    Load and return the full parsed YAML document.

    Supported current formats:

    Old format:
        project:
          name: MyApp
        plugins:
          - react
          - fastapi
          - postgres

    New format:
        kind: project
        name: MyApp
        uses:
          stack: web-stack
          app: finance-dashboard
        overrides:
          postgres:
            db: finance_app
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Stack file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    if not isinstance(data, dict):
        raise RuntimeError("YAML document must parse to a mapping/object at the root")

    kind = detect_kind(data)

    # Only normalize known kinds here.
    # Unknown docs are returned raw so the caller can decide what to do.
    if kind != "unknown":
        try:
            data = validate_and_normalize_document(data, kind)
        except ValidationError as e:
            raise RuntimeError(f"Invalid {kind} document in {path}: {e}") from e

    return data


def detect_kind(doc):
    """
    Detect document kind.

    Explicit kinds:
    - stack
    - app
    - project

    Backward-compatible fallback:
    - stack-legacy if plugins are present and no kind is declared
    """
    kind = doc.get("kind")
    if kind:
        return kind

    if "plugins" in doc:
        return "stack-legacy"

    return "unknown"


def resolve_project_name(doc):
    """
    Resolve the project name from either the new or old format.

    New format:
        kind: project
        name: MyApp

    Old format:
        project:
          name: MyApp
    """
    kind = detect_kind(doc)

    if kind == "project":
        name = doc.get("name")
        if name:
            return name

    project = doc.get("project", {})
    if isinstance(project, dict):
        name = project.get("name")
        if name:
            return name

    name = doc.get("name")
    if name:
        return name

    return "MyApp"


def get_plugin_names(doc):
    """
    Return plugin names from a document.

    Current behavior:
    - stack-legacy documents read plugins directly
    - stack documents read plugins directly
    - resolved project documents may also expose plugins directly

    Future:
    - kind: project should usually resolve plugins through preset resolution
    """
    plugins = doc.get("plugins", [])

    if not isinstance(plugins, list):
        raise RuntimeError("'plugins' must be a list when present")

    return plugins