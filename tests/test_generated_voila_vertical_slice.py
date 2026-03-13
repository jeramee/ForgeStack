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
    assert "Open Voilà View" in frontend_app
    assert "config?.voila?.enabled" in frontend_app

    assert '"nbformat": 4' in voila_demo
    assert "Hello from the ForgeStack Voilà view bridge" in voila_demo