from forgestack.core.registry import PluginRegistry
from forgestack.core.planner import create_plan
from forgestack.core.stack_loader import load_stack_yaml, get_plugin_names
from forgestack.core.preset_resolver import resolve_document
from forgestack.cli.main import _build_render_context
from forgestack.core.plan_executor import execute_plan


def test_generated_jupyter_vertical_slice(tmp_path):
    raw_doc = load_stack_yaml("projects/DataWorkbenchApp.yaml")
    effective_doc = resolve_document(raw_doc)
    plugin_names = get_plugin_names(effective_doc)
    render_context = _build_render_context(raw_doc, effective_doc)

    registry = PluginRegistry()
    registry.discover()

    _, plan = create_plan(plugin_names, registry, render_context=render_context)
    output_root = tmp_path / "DataWorkbenchApp"
    execute_plan(plan, output_root=output_root)

    app_config = (output_root / "backend" / "app_config.py").read_text(encoding="utf-8")
    compose = (output_root / "docker-compose.yml").read_text(encoding="utf-8")
    frontend_app = (output_root / "frontend" / "src" / "App.jsx").read_text(encoding="utf-8")
    notebooks_readme = (output_root / "notebooks" / "README.md").read_text(encoding="utf-8")

    env_example = (output_root / ".env.example").read_text(encoding="utf-8")
    readme = (output_root / "README.md").read_text(encoding="utf-8")


    assert '"project_name": "DataWorkbenchApp"' in app_config
    assert '"app_name": "data-workbench"' in app_config
    assert '"jupyter": {' in app_config
    assert '"enabled": True' in app_config
    assert '"port": 8888' in app_config

    assert "jupyter:" in compose
    assert "jupyter/base-notebook:python-3.11" in compose
    assert '"8888:8888"' in compose

    assert "Data Workbench" in frontend_app
    assert "Notebook Workspace" in frontend_app
    assert "config?.jupyter?.enabled" in frontend_app
    assert "Open Jupyter Workspace" in frontend_app

    assert "# Notebooks" in notebooks_readme

    assert "JUPYTER_PORT=8888" in env_example
    assert "POSTGRES_" not in env_example
    assert "REDIS_" not in env_example

    assert "- Notebook Workspace: Jupyter" in readme
    assert "- Database: SQLite" in readme
    assert "- Cache/Queue: Redis" not in readme
    assert "- Worker: Celery" not in readme
