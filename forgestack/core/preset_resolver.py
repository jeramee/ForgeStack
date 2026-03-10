from pathlib import Path

from forgestack.core.stack_loader import load_stack_yaml, detect_kind


PRESETS_ROOT = Path("presets")
STACK_PRESETS_DIR = PRESETS_ROOT / "stack"
APP_PRESETS_DIR = PRESETS_ROOT / "app"


def _load_named_preset(base_dir: Path, name: str) -> dict:
    path = base_dir / f"{name}.yaml"

    if not path.exists():
        raise FileNotFoundError(f"Preset not found: {path}")

    doc = load_stack_yaml(path)

    if not isinstance(doc, dict):
        raise RuntimeError(f"Preset file must parse to a mapping: {path}")

    return doc


def load_stack_preset(name: str) -> dict:
    doc = _load_named_preset(STACK_PRESETS_DIR, name)

    kind = detect_kind(doc)
    if kind not in {"stack", "stack-legacy"}:
        raise RuntimeError(f"Preset '{name}' is not a stack preset")

    return doc


def load_app_preset(name: str) -> dict:
    doc = _load_named_preset(APP_PRESETS_DIR, name)

    kind = detect_kind(doc)
    if kind != "app":
        raise RuntimeError(f"Preset '{name}' is not an app preset")

    return doc


def _merge_unique_lists(*lists):
    seen = set()
    result = []

    for items in lists:
        for item in items or []:
            if item not in seen:
                seen.add(item)
                result.append(item)

    return result


def resolve_project_document(project_doc: dict) -> dict:
    """
    Resolve a project document into an effective stack-like document.

    Input:
        kind: project
        name: MyApp
        uses:
          stack: web-stack
          app: finance-dashboard
        overrides:
          postgres:
            db: finance_app

    Output:
        {
            "kind": "resolved-project",
            "name": "MyApp",
            "plugins": [...],
            "stack": {...},
            "app": {...},
            "overrides": {...},
        }
    """
    if detect_kind(project_doc) != "project":
        raise RuntimeError("resolve_project_document() requires a kind: project document")

    name = project_doc.get("name") or "MyApp"

    uses = project_doc.get("uses", {})
    if not isinstance(uses, dict):
        raise RuntimeError("'uses' must be a mapping in a project document")

    stack_name = uses.get("stack")
    app_name = uses.get("app")

    if not stack_name:
        raise RuntimeError("Project document must declare uses.stack")

    if not app_name:
        raise RuntimeError("Project document must declare uses.app")

    stack_doc = load_stack_preset(stack_name)
    app_doc = load_app_preset(app_name)

    stack_plugins = stack_doc.get("plugins", [])
    app_plugins = app_doc.get("plugins", [])

    if not isinstance(stack_plugins, list):
        raise RuntimeError(f"Stack preset '{stack_name}' has invalid plugins list")

    if not isinstance(app_plugins, list):
        raise RuntimeError(f"App preset '{app_name}' has invalid plugins list")

    plugins = _merge_unique_lists(stack_plugins, app_plugins)

    overrides = project_doc.get("overrides", {})
    if overrides is None:
        overrides = {}

    if not isinstance(overrides, dict):
        raise RuntimeError("'overrides' must be a mapping")

    return {
        "kind": "resolved-project",
        "name": name,
        "plugins": plugins,
        "stack": stack_doc,
        "app": app_doc,
        "overrides": overrides,
    }


def resolve_document(doc: dict) -> dict:
    """
    Resolve any supported document into an effective planning document.

    Current behavior:
    - stack-legacy => use directly
    - stack        => use directly
    - app          => not directly plannable
    - project      => resolve stack + app + overrides
    """
    kind = detect_kind(doc)

    if kind in {"stack", "stack-legacy"}:
        return doc

    if kind == "project":
        return resolve_project_document(doc)

    if kind == "app":
        raise RuntimeError("App presets are not directly plannable; create or apply a project instead")

    raise RuntimeError(f"Unsupported document kind: {kind}")