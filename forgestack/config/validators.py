from __future__ import annotations

from copy import deepcopy


class ValidationError(RuntimeError):
    """Raised when a ForgeStack document fails schema validation."""


def _ensure_mapping(value, label: str) -> dict:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be a mapping")
    return value


def _ensure_nonempty_string(value, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label} must be a non-empty string")
    return value.strip()


def _ensure_string_list(value, label: str) -> list[str]:
    if value is None:
        return []

    if not isinstance(value, list):
        raise ValidationError(f"{label} must be a list")

    result: list[str] = []
    for i, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise ValidationError(f"{label}[{i}] must be a non-empty string")
        result.append(item.strip())

    return result


def normalize_stack_doc(doc: dict, *, legacy: bool = False) -> dict:
    result = deepcopy(doc)

    name = result.get("name")
    if name is not None:
        name = _ensure_nonempty_string(name, "stack.name")

    plugins = _ensure_string_list(result.get("plugins", []), "stack.plugins")
    defaults = _ensure_mapping(result.get("defaults", {}), "stack.defaults")

    capabilities = result.get("capabilities", [])
    if capabilities is None:
        capabilities = []
    elif not isinstance(capabilities, list):
        raise ValidationError("stack.capabilities must be a list")

    service_profile = _ensure_mapping(
        result.get("service_profile", {}), "stack.service_profile"
    )

    result["kind"] = "stack-legacy" if legacy else "stack"
    result["plugins"] = plugins
    result["defaults"] = defaults
    result["capabilities"] = capabilities
    result["service_profile"] = service_profile

    if name is not None:
        result["name"] = name

    return result

def _ensure_feature_mapping(value, label: str) -> dict:
    if value is None:
        return {}

    if isinstance(value, dict):
        result = {}
        for key, enabled in value.items():
            if not isinstance(key, str) or not key.strip():
                raise ValidationError(f"{label} keys must be non-empty strings")
            result[key.strip()] = bool(enabled)
        return result

    if isinstance(value, list):
        result = {}
        for i, item in enumerate(value):
            if not isinstance(item, str) or not item.strip():
                raise ValidationError(f"{label}[{i}] must be a non-empty string")
            result[item.strip()] = True
        return result

    raise ValidationError(f"{label} must be a mapping or a list of strings")

def normalize_app_doc(doc: dict) -> dict:
    result = deepcopy(doc)

    name = _ensure_nonempty_string(result.get("name"), "app.name")
    plugins = _ensure_string_list(result.get("plugins", []), "app.plugins")
    defaults = _ensure_mapping(result.get("defaults", {}), "app.defaults")
    features = _ensure_feature_mapping(result.get("features", {}), "app.features")
    ui = _ensure_mapping(result.get("ui", {}), "app.ui")

    # Accept legacy/alias field "stack", normalize to "default_stack"
    default_stack = result.get("default_stack", result.get("stack"))
    if default_stack is not None:
        default_stack = _ensure_nonempty_string(default_stack, "app.default_stack")

    result["kind"] = "app"
    result["name"] = name
    result["plugins"] = plugins
    result["defaults"] = defaults
    result["features"] = features
    result["ui"] = ui

    if default_stack is not None:
        result["default_stack"] = default_stack

    # Remove alias from normalized output
    result.pop("stack", None)

    return result


def normalize_project_doc(doc: dict) -> dict:
    result = deepcopy(doc)

    name = _ensure_nonempty_string(result.get("name"), "project.name")
    uses = _ensure_mapping(result.get("uses", {}), "project.uses")
    overrides = _ensure_mapping(result.get("overrides", {}), "project.overrides")

    stack_name = _ensure_nonempty_string(uses.get("stack"), "project.uses.stack")
    app_name = _ensure_nonempty_string(uses.get("app"), "project.uses.app")

    result["kind"] = "project"
    result["name"] = name
    result["uses"] = {
        "stack": stack_name,
        "app": app_name,
    }
    result["overrides"] = overrides

    return result


def normalize_resolved_project_doc(doc: dict) -> dict:
    result = deepcopy(doc)

    name = _ensure_nonempty_string(result.get("name"), "resolved-project.name")
    plugins = _ensure_string_list(result.get("plugins", []), "resolved-project.plugins")
    stack = _ensure_mapping(result.get("stack"), "resolved-project.stack")
    app = _ensure_mapping(result.get("app"), "resolved-project.app")
    project = _ensure_mapping(result.get("project"), "resolved-project.project")
    values = _ensure_mapping(result.get("values", {}), "resolved-project.values")

    result["kind"] = "resolved-project"
    result["name"] = name
    result["plugins"] = plugins
    result["stack"] = stack
    result["app"] = app
    result["project"] = project
    result["values"] = values

    return result


def validate_and_normalize_document(doc: dict, kind: str) -> dict:
    if not isinstance(doc, dict):
        raise ValidationError("Document root must be a mapping")

    if kind == "stack":
        normalized = normalize_stack_doc(doc, legacy=False)
        if doc.get("kind") not in {None, "stack"}:
            raise ValidationError("stack.kind must be 'stack'")
        return normalized

    if kind == "stack-legacy":
        return normalize_stack_doc(doc, legacy=True)

    if kind == "app":
        if doc.get("kind") not in {None, "app"}:
            raise ValidationError("app.kind must be 'app'")
        return normalize_app_doc(doc)

    if kind == "project":
        if doc.get("kind") not in {None, "project"}:
            raise ValidationError("project.kind must be 'project'")
        return normalize_project_doc(doc)

    if kind == "resolved-project":
        if doc.get("kind") not in {None, "resolved-project"}:
            raise ValidationError("resolved-project.kind must be 'resolved-project'")
        return normalize_resolved_project_doc(doc)

    raise ValidationError(f"Unsupported document kind: {kind}")