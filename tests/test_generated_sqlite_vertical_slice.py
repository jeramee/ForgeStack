from forgestack.core.registry import PluginRegistry
from forgestack.core.planner import create_plan
from forgestack.core.stack_loader import load_stack_yaml, get_plugin_names
from forgestack.core.preset_resolver import resolve_document
from forgestack.cli.main import _build_render_context
from forgestack.core.plan_executor import execute_plan


def test_generated_sqlite_vertical_slice(tmp_path):
    raw_doc = load_stack_yaml("projects/LocalWorkflowApp.yaml")
    effective_doc = resolve_document(raw_doc)
    plugin_names = get_plugin_names(effective_doc)
    render_context = _build_render_context(raw_doc, effective_doc)

    registry = PluginRegistry()
    registry.discover()

    _, plan = create_plan(plugin_names, registry, render_context=render_context)
    output_root = tmp_path / "LocalWorkflowApp"
    execute_plan(plan, output_root=output_root)

    backend_main = (output_root / "backend" / "main.py").read_text(encoding="utf-8")
    app_config = (output_root / "backend" / "app_config.py").read_text(encoding="utf-8")
    db_py = (output_root / "backend" / "db.py").read_text(encoding="utf-8")
    compose = (output_root / "docker-compose.yml").read_text(encoding="utf-8")

    assert "from db import get_connection, init_db" in backend_main
    assert '@app.get("/items")' in backend_main
    assert '@app.post("/items/seed")' in backend_main
    assert "init_db()" in backend_main

    assert '"project_name": "LocalWorkflowApp"' in app_config
    assert '"stack_name": "local-workflow-stack"' in app_config
    assert '"app_name": "local-workflow-console"' in app_config
    assert '"sqlite": {' in app_config
    assert '"enabled": True' in app_config
    assert '"database": "app.db"' in app_config

    assert "sqlite3.connect" in db_py
    assert "CREATE TABLE IF NOT EXISTS items" in db_py

    assert "frontend:" in compose
    assert "backend:" in compose
    assert "postgres:" not in compose
    assert "redis:" not in compose
    assert "celery:" not in compose