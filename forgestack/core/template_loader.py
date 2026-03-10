from pathlib import Path
from jinja2 import Template


TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def candidate_template_paths(template_name: str) -> list[Path]:
    return [
        TEMPLATES_DIR / template_name,
        TEMPLATES_DIR / f"{template_name}.txt",
        TEMPLATES_DIR / f"{template_name}.py",
        TEMPLATES_DIR / f"{template_name}.json",
        TEMPLATES_DIR / f"{template_name}.yml",
        TEMPLATES_DIR / f"{template_name}.yaml",
        TEMPLATES_DIR / f"{template_name}.md",
    ]


def load_template_text(template_name: str) -> str:
    for path in candidate_template_paths(template_name):
        if path.exists():
            return path.read_text(encoding="utf-8")

    tried = "\n".join(str(p) for p in candidate_template_paths(template_name))
    raise FileNotFoundError(
        f"Template '{template_name}' not found.\nTried:\n{tried}"
    )


def render_template_text(template_name: str, context: dict | None = None) -> str:
    raw = load_template_text(template_name)
    template = Template(raw)
    return template.render(**(context or {}))