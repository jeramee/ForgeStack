from pathlib import Path

from forgestack.core.registry import PluginRegistry
from forgestack.core.planner import create_plan
from forgestack.core.stack_loader import load_stack_yaml, get_plugin_names
from forgestack.core.preset_resolver import resolve_document
from forgestack.cli.main import _build_render_context
from forgestack.core.plan_executor import execute_plan


def test_full_build_plan_outputs(tmp_path):
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
    frontend_app = (output_root / "frontend" / "src" / "App.jsx").read_text(encoding="utf-8")
    frontend_shell = (output_root / "frontend" / "src" / "generated" / "AppShell.jsx").read_text(encoding="utf-8")
    app_config = (output_root / "backend" / "app_config.py").read_text(encoding="utf-8")

    # Existing/full-stack output sanity
    assert (output_root / "backend" / "requirements.txt").exists()
    assert (output_root / "backend" / "Dockerfile").exists()
    assert (output_root / "frontend" / "package.json").exists()
    assert (output_root / "frontend" / "Dockerfile").exists()
    assert (output_root / "docker-compose.yml").exists()

    # Config contract
    assert '"project_name": "MyApp"' in app_config
    assert '"stack_name": "web-stack"' in app_config
    assert '"app_name": "finance-dashboard"' in app_config
    assert '"charts": True' in app_config
    assert '"auth": True' in app_config

    # M7 backend async flow
    assert '@app.post("/tasks/ping")' in backend_main
    assert '@app.get("/tasks/{task_id}")' in backend_main
    assert "AsyncResult" in backend_main
    assert "task.ready()" in backend_main
    assert "task.successful()" in backend_main
    assert 'payload["result"]' in backend_main

    # M7 frontend async flow
    assert "import AppShell from './generated/AppShell'" in frontend_app
    assert "return <AppShell />" in frontend_app

    assert "/config" in frontend_shell
    assert "/tasks/ping" in frontend_shell
    assert "/tasks/${taskId}" in frontend_shell
    assert "setInterval" in frontend_shell
    assert "setTaskState" in frontend_shell
    assert "setTaskResult" in frontend_shell
    
    compose = (output_root / "docker-compose.yml").read_text(encoding="utf-8")
    env_example = (output_root / ".env.example").read_text(encoding="utf-8")
    readme = (output_root / "README.md").read_text(encoding="utf-8")

    assert '"5432:5432"' not in compose
    assert '"6379:6379"' not in compose
    assert "POSTGRES_DB=" in env_example
    assert "REDIS_PORT=" in env_example
    assert "- Database: PostgreSQL" in readme
    assert "- Worker: Celery" in readme

    assert "## Run" in readme
    assert "```powershell" in readme

    assert "postgres:" in compose
    assert "redis:" in compose
    assert "celery:" in compose

    assert "- Frontend: React" in readme
    assert "- Backend: FastAPI" in readme
    assert "- Cache/Queue: Redis" in readme
    assert "docker compose up --build" in readme
