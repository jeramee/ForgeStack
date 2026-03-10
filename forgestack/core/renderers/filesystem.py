from __future__ import annotations

from pathlib import Path

from ..models import StackModel


class FilesystemRenderer:
    def render(self, model: StackModel, root: str) -> None:
        root_path = Path(root)
        root_path.mkdir(parents=True, exist_ok=True)

        for file in model.files:
            out = root_path / file.path
            out.parent.mkdir(parents=True, exist_ok=True)

            if file.mode == "append" and out.exists():
                existing = out.read_text(encoding="utf-8")
                if file.content not in existing:
                    out.write_text(existing + file.content, encoding="utf-8")
            else:
                out.write_text(file.content, encoding="utf-8")
