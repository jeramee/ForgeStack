from __future__ import annotations

from pathlib import Path

from ..models import StackModel


class DocsRenderer:
    def render(self, model: StackModel, root: str) -> None:
        lines = [
            f"# Stack: {model.name}",
            "",
            "## Plugins",
        ]
        lines.extend(f"- {name}" for name in model.resolved_plugins)
        lines.extend([
            "",
            "## Capabilities",
        ])
        lines.extend(f"- {cap}" for cap in sorted(model.capabilities))
        lines.extend([
            "",
            "## Services",
        ])
        lines.extend(f"- {name}" for name in sorted(model.services.keys()))
        lines.extend([
            "",
            "## Files",
        ])
        lines.extend(f"- {file.path}" for file in model.files)
        out = Path(root) / "STACK.md"
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
