from pathlib import Path

from forgestack.core.registry import PluginRegistry
from forgestack.core.planner import create_plan
from forgestack.core.stack_loader import load_stack_yaml, get_plugin_names
from forgestack.core.preset_resolver import resolve_document
from forgestack.cli.main import _build_render_context
from forgestack.core.plan_executor import execute_plan


def test_generated_async_vertical_slice(tmp_path):
    raw_doc = load_stack_yaml("projects/MyApp.yaml")
    effective_doc = resolve_document(raw_doc)
    plugin_names = get_plugin_names(effective_doc)
    render_context = _build_render_context(raw_doc, effective_doc)

    registry = PluginRegistry()
    registry.discover()

    _, plan = create_plan(plugin_names, registry, render_context=render_context)
    output_root = tmp_path / "MyApp"
    execute_plan(plan, output_root=output_root)

    backend_main = (output_root / "backend" / "main.py").read_text(encoding="utf-8")
    frontend_shell = (output_root / "frontend" / "src" / "generated" / "AppShell.jsx").read_text(encoding="utf-8")
    celery_tasks = (output_root / "backend" / "tasks.py").read_text(encoding="utf-8")

    # Backend should expose queue + polling endpoints
    assert '@app.post("/tasks/ping")' in backend_main
    assert '@app.get("/tasks/{task_id}")' in backend_main
    assert "from celery.result import AsyncResult" in backend_main
    assert "from celery_app import celery_app" in backend_main

    # Task implementation should still exist
    assert "@celery_app.task" in celery_tasks
    assert "def ping()" in celery_tasks
    assert '"worker": "celery"' in celery_tasks

    # Frontend should fetch config, queue task, and poll for result
    assert "fetch(`${API_BASE}/config`)" in frontend_shell
    assert "fetch(`${API_BASE}/tasks/ping`" in frontend_shell
    assert "fetch(`${API_BASE}/tasks/${taskId}`)" in frontend_shell
    assert "setInterval" in frontend_shell
    assert "setTaskId" in frontend_shell
    assert "setTaskState" in frontend_shell
    assert "setTaskResult" in frontend_shell