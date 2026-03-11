from pathlib import Path
from jinja2 import Template


TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


TEMPLATE_ALIASES = {
    "react_package": "react/package.json",
    "python_requirements": "python/requirements.txt",
    "root_docker_compose": "root/docker-compose.yml",
    "postgres_docker": "docker/postgres.yml",
    "redis_docker": "docker/redis.yml",
    "celery_app": "celery/app.py",
    "celery_tasks": "celery/tasks.py",
    "celery_docker": "docker/celery.yml",
    "fastapi_main": "fastapi/main.py",
}


def _canonical_template_name(template_name: str) -> str:
    return TEMPLATE_ALIASES.get(template_name, template_name)


def _paths_for_name(template_name: str) -> list[Path]:
    return [
        TEMPLATES_DIR / template_name,
        TEMPLATES_DIR / f"{template_name}.txt",
        TEMPLATES_DIR / f"{template_name}.py",
        TEMPLATES_DIR / f"{template_name}.json",
        TEMPLATES_DIR / f"{template_name}.yml",
        TEMPLATES_DIR / f"{template_name}.yaml",
        TEMPLATES_DIR / f"{template_name}.md",
    ]


def candidate_template_paths(template_name: str) -> list[Path]:
    canonical_name = _canonical_template_name(template_name)

    paths = _paths_for_name(canonical_name)

    if canonical_name != template_name:
        paths.extend(_paths_for_name(template_name))

    return paths


def load_template_text(template_name: str) -> str:
    paths = candidate_template_paths(template_name)

    for path in paths:
        if path.exists():
            return path.read_text(encoding="utf-8")

    tried = "\n".join(str(p) for p in paths)
    canonical_name = _canonical_template_name(template_name)
    raise FileNotFoundError(
        f"Template '{template_name}' not found (canonical: '{canonical_name}').\nTried:\n{tried}"
    )


def render_template_text(template_name: str, context: dict | None = None) -> str:
    raw = load_template_text(template_name)
    template = Template(raw)
    return template.render(**(context or {}))