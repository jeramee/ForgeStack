from pathlib import Path
from copy import deepcopy

from forgestack.config.validators import (
    ValidationError,
    validate_and_normalize_document,
)
from forgestack.core.stack_loader import load_stack_yaml, detect_kind


PRESETS_ROOT = Path("presets")
STACK_PRESETS_DIR = PRESETS_ROOT / "stack"
APP_PRESETS_DIR = PRESETS_ROOT / "app"


def _load_named_preset(base_dir: Path, name: str, expected_kind: str) -> dict:
    path = base_dir / f"{name}.yaml"

    if not path.exists():
        raise FileNotFoundError(f"Preset not found: {path}")

    doc = load_stack_yaml(path)

    try:
        doc = validate_and_normalize_document(doc, expected_kind)
    except ValidationError as e:
        raise RuntimeError(
            f"Invalid {expected_kind} document in {path}: {e}"
        ) from e

    return doc


def load_stack_preset(name: str, presets_root: Path = STACK_PRESETS_DIR) -> dict:
    return _load_named_preset(presets_root, name, "stack")


def load_app_preset(name: str, presets_root: Path = APP_PRESETS_DIR) -> dict:
    return _load_named_preset(presets_root, name, "app")


def _merge_unique_lists(*lists):
    seen = set()
    result = []

    for items in lists:
        for item in items or []:
            if item not in seen:
                seen.add(item)
                result.append(item)

    return result


def _deep_merge(base: dict, override: dict) -> dict:
    result = deepcopy(base)

    for key, value in (override or {}).items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = deepcopy(value)

    return result


def _build_effective_values(stack_doc: dict, app_doc: dict, project_doc: dict) -> dict:
    stack_defaults = stack_doc.get("defaults", {})
    app_defaults = app_doc.get("defaults", {})
    project_overrides = project_doc.get("overrides", {})

    values = _deep_merge(stack_defaults, app_defaults)
    values = _deep_merge(values, project_overrides)
    return values


def resolve_project_document(project_doc: dict, base_dir: Path | str = ".") -> dict:
    base_dir = Path(base_dir)
    stack_presets_dir = base_dir / "presets" / "stack"
    app_presets_dir = base_dir / "presets" / "app"

    try:
        project_doc = validate_and_normalize_document(project_doc, "project")
    except ValidationError as e:
        raise RuntimeError(f"Invalid project document: {e}") from e

    stack_name = project_doc["uses"]["stack"]
    app_name = project_doc["uses"]["app"]

    stack_doc = load_stack_preset(stack_name, stack_presets_dir)
    app_doc = load_app_preset(app_name, app_presets_dir)

    stack_plugins = stack_doc.get("plugins", [])
    app_plugins = app_doc.get("plugins", [])

    plugins = _merge_unique_lists(stack_plugins, app_plugins)
    values = _build_effective_values(stack_doc, app_doc, project_doc)

    resolved = {
        "kind": "resolved-project",
        "name": project_doc["name"],
        "plugins": plugins,
        "stack": stack_doc,
        "app": app_doc,
        "project": project_doc,
        "values": values,
    }

    try:
        return validate_and_normalize_document(resolved, "resolved-project")
    except ValidationError as e:
        raise RuntimeError(
            f"Internal error: invalid resolved-project for '{project_doc['name']}': {e}"
        ) from e


def resolve_document(doc: dict) -> dict:
    kind = detect_kind(doc)

    if kind in {"stack", "stack-legacy"}:
        try:
            return validate_and_normalize_document(doc, kind)
        except ValidationError as e:
            raise RuntimeError(f"Invalid {kind} document: {e}") from e

    if kind == "project":
        return resolve_project_document(doc)

    if kind == "app":
        raise RuntimeError(
            "App presets are not directly plannable; create or apply a project instead"
        )

    raise RuntimeError(f"Unsupported document kind: {kind}")