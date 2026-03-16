from forgestack.core.registry import PluginRegistry
from forgestack.core.planner import create_plan
from forgestack.core.stack_loader import load_stack_yaml, get_plugin_names
from forgestack.core.preset_resolver import resolve_document
from forgestack.cli.main import _build_render_context
from forgestack.core.plan_executor import execute_plan


def _generate(project_path: str, tmp_path, output_name: str):
    raw_doc = load_stack_yaml(project_path)
    effective_doc = resolve_document(raw_doc)
    plugin_names = get_plugin_names(effective_doc)
    render_context = _build_render_context(raw_doc, effective_doc)

    registry = PluginRegistry()
    registry.discover()

    _, plan = create_plan(plugin_names, registry, render_context=render_context)
    output_root = tmp_path / output_name
    execute_plan(plan, output_root=output_root)
    return output_root


def test_web_stack_root_artifacts(tmp_path):
    output_root = _generate("projects/MyApp.yaml", tmp_path, "MyApp")

    compose = (output_root / "docker-compose.yml").read_text(encoding="utf-8")
    env_example = (output_root / ".env.example").read_text(encoding="utf-8")
    readme = (output_root / "README.md").read_text(encoding="utf-8")
    gitignore = (output_root / ".gitignore").read_text(encoding="utf-8")

    assert "frontend:" in compose
    assert "backend:" in compose
    assert "postgres:" in compose
    assert "redis:" in compose
    assert "celery:" in compose

    assert '"5432:5432"' not in compose
    assert '"6379:6379"' not in compose

    assert "POSTGRES_DB=" in env_example
    assert "POSTGRES_PORT=" in env_example
    assert "REDIS_PORT=" in env_example

    assert "- Frontend: React" in readme
    assert "- Backend: FastAPI" in readme
    assert "- Database: PostgreSQL" in readme
    assert "- Cache/Queue: Redis" in readme
    assert "- Worker: Celery" in readme

    assert ".venv/" in gitignore
    assert "node_modules/" in gitignore
    assert ".env" in gitignore


def test_sqlite_stack_root_artifacts(tmp_path):
    output_root = _generate("projects/LocalWorkflowApp.yaml", tmp_path, "LocalWorkflowApp")

    env_example = (output_root / ".env.example").read_text(encoding="utf-8")
    readme = (output_root / "README.md").read_text(encoding="utf-8")

    assert "POSTGRES_" not in env_example
    assert "REDIS_" not in env_example

    assert "- Database: SQLite" in readme
    assert "- Cache/Queue: Redis" not in readme
    assert "- Worker: Celery" not in readme


def test_notebook_view_root_artifacts(tmp_path):
    output_root = _generate("projects/NotebookViewApp.yaml", tmp_path, "NotebookViewApp")

    env_example = (output_root / ".env.example").read_text(encoding="utf-8")
    readme = (output_root / "README.md").read_text(encoding="utf-8")

    assert "JUPYTER_PORT=" in env_example
    assert "VOILA_PORT=" in env_example

    assert "- Notebook Workspace: Jupyter" in readme
    assert "- Notebook View: Voila" in readme