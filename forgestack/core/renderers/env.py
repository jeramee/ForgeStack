from __future__ import annotations

from pathlib import Path

from ..models import StackModel


class EnvRenderer:
    def render(self, model: StackModel, root: str) -> None:
        lines = [f"{k}={v}" for k, v in sorted(model.env.items())]
        out = Path(root) / ".env.example"
        out.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
