from forgestack.core.registry import PluginRegistry
from forgestack.core.planner import create_plan
from forgestack.core.stack_loader import load_stack_yaml, get_plugin_names
from forgestack.core.preset_resolver import resolve_document
from forgestack.cli.main import _build_render_context
from forgestack.core.plan_executor import execute_plan


def test_generated_technician_console_vertical_slice(tmp_path):
    raw_doc = load_stack_yaml("projects/TechnicianConsoleApp.yaml")
    effective_doc = resolve_document(raw_doc)
    plugin_names = get_plugin_names(effective_doc)
    render_context = _build_render_context(raw_doc, effective_doc)

    registry = PluginRegistry()
    registry.discover()

    _, plan = create_plan(plugin_names, registry, render_context=render_context)
    output_root = tmp_path / "TechnicianConsoleApp"
    execute_plan(plan, output_root=output_root)

    app_config = (output_root / "backend" / "app_config.py").read_text(encoding="utf-8")
    frontend_app = (output_root / "frontend" / "src" / "App.jsx").read_text(encoding="utf-8")

    assert '"project_name": "TechnicianConsoleApp"' in app_config
    assert '"app_name": "technician-console"' in app_config
    assert '"technician_console": True' in app_config
    assert '"quick_actions": True' in app_config

    assert "Technician Console" in frontend_app
    assert "Queue Summary" in frontend_app
    assert "Quick Actions" in frontend_app
    assert "Work Items" in frontend_app
    assert "/items" in frontend_app
    assert "/items/seed" in frontend_app