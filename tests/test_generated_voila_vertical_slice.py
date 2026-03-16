from forgestack.core.registry import PluginRegistry
from forgestack.core.planner import create_plan
from forgestack.core.stack_loader import load_stack_yaml, get_plugin_names
from forgestack.core.preset_resolver import resolve_document
from forgestack.cli.main import _build_render_context
from forgestack.core.plan_executor import execute_plan


def test_generated_voila_vertical_slice(tmp_path):
    raw_doc = load_stack_yaml("projects/NotebookViewApp.yaml")
    effective_doc = resolve_document(raw_doc)
    plugin_names = get_plugin_names(effective_doc)
    render_context = _build_render_context(raw_doc, effective_doc)

    registry = PluginRegistry()
    registry.discover()

    _, plan = create_plan(plugin_names, registry, render_context=render_context)
    output_root = tmp_path / "NotebookViewApp"
    execute_plan(plan, output_root=output_root)

    app_config = (output_root / "backend" / "app_config.py").read_text(encoding="utf-8")
    compose = (output_root / "docker-compose.yml").read_text(encoding="utf-8")
    frontend_app = (output_root / "frontend" / "src" / "App.jsx").read_text(encoding="utf-8")
    voila_demo = (output_root / "notebooks" / "voila_demo.ipynb").read_text(encoding="utf-8")

    env_example = (output_root / ".env.example").read_text(encoding="utf-8")
    readme = (output_root / "README.md").read_text(encoding="utf-8")


    assert '"project_name": "NotebookViewApp"' in app_config
    assert '"app_name": "notebook-view"' in app_config
    assert '"voila": {' in app_config
    assert '"enabled": True' in app_config
    assert '"port": 8866' in app_config

    assert "voila:" in compose
    assert "pip install voila" in compose
    assert "voila /home/jovyan/work/voila_demo.ipynb" in compose
    assert '"8866:8866"' in compose

    assert "Notebook View Bridge" in frontend_app
    assert "Open Voila View" in frontend_app
    assert "config?.voila?.enabled" in frontend_app

    assert '"nbformat": 4' in voila_demo
    assert "Hello from the ForgeStack Voila view bridge" in voila_demo

    assert "JUPYTER_PORT=8888" in env_example
    assert "VOILA_PORT=8866" in env_example
    assert "POSTGRES_" not in env_example
    assert "REDIS_" not in env_example

    assert "- Notebook Workspace: Jupyter" in readme
    assert "- Notebook View: Voila" in readme
    assert "- Database: SQLite" in readme
    assert "- Cache/Queue: Redis" not in readme
    assert "- Worker: Celery" not in readme

    assert "POSTGRES_" not in env_example
    assert "REDIS_" not in env_example

    assert "- Database: SQLite" in readme
    assert "- Cache/Queue: Redis" not in readme
    assert "- Worker: Celery" not in readme

