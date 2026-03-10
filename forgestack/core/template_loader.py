from pathlib import Path


TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def candidate_template_paths(template_name: str) -> list[Path]:
    """
    Try a few common filename patterns for a logical template name.
    """
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
    """
    Load a template by logical name from forgestack/templates.
    """
    for path in candidate_template_paths(template_name):
        if path.exists():
            return path.read_text(encoding="utf-8")

    tried = "\n".join(str(p) for p in candidate_template_paths(template_name))
    raise FileNotFoundError(
        f"Template '{template_name}' not found.\nTried:\n{tried}"
    )