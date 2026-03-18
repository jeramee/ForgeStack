from forgestack.core.registry import PluginRegistry
from forgestack.core.planner import create_plan


def test_react_scaffold_includes_protected_wrapper_and_generated_shell():
    registry = PluginRegistry()
    registry.discover()

    _, plan = create_plan(["react"], registry)

    paths = {
        action["path"]
        for action in plan.actions
        if action["type"] == "create_file"
    }

    assert "frontend/src/main.jsx" in paths
    assert "frontend/src/App.jsx" in paths
    assert "frontend/src/generated/AppShell.jsx" in paths
    