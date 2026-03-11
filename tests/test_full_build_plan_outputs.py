from forgestack.core.registry import PluginRegistry
from forgestack.core.planner import create_plan


def test_full_build_plan_contains_expanded_outputs():
    registry = PluginRegistry()
    registry.discover()

    plugin_names = ["react", "python", "fastapi", "postgres", "redis", "celery"]
    render_context = {
        "project_name": "MyApp",
        "features": {
            "charts": True,
            "filters": True,
            "reporting": True,
            "auth": True,
            "admin": True,
        },
        "has_feature": {
            "charts": True,
            "filters": True,
            "reporting": True,
            "auth": True,
            "admin": True,
        },
    }

    _, plan = create_plan(plugin_names, registry, render_context=render_context)

    paths = [a["path"] for a in plan.actions if a["type"] == "create_file"]

    assert "frontend/package.json" in paths
    assert "frontend/index.html" in paths
    assert "frontend/src/main.jsx" in paths
    assert "frontend/src/App.jsx" in paths
    assert "backend/requirements.txt" in paths
    assert "backend/main.py" in paths
    assert "backend/app_config.py" in paths
    assert "README.md" in paths
    assert ".env.example" in paths
    assert ".gitignore" in paths
    assert "docker-compose.yml" in paths