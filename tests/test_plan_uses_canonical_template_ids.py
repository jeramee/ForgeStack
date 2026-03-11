from forgestack.core.registry import PluginRegistry
from forgestack.core.planner import create_plan


def test_plan_uses_canonical_template_ids():
    registry = PluginRegistry()
    registry.discover()

    plugin_names = ["react", "python", "postgres", "redis", "celery", "fastapi"]
    render_context = {
        "project_name": "MyApp",
        "has_feature": {
            "charts": True,
            "filters": True,
        },
    }

    _, plan = create_plan(plugin_names, registry, render_context=render_context)

    templates = [a.get("template") for a in plan.actions if a["type"] == "create_file"]

    assert "react/package.json" in templates
    assert "python/requirements.txt" in templates
    assert "docker/postgres.yml" in templates
    assert "docker/redis.yml" in templates
    assert "celery/app.py" in templates
    assert "celery/tasks.py" in templates
    assert "docker/celery.yml" in templates
    assert "fastapi/main.py" in templates