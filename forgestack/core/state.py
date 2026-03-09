from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass(slots=True)
class AppliedFileRecord:
    path: str
    checksum: str
    plugin: str | None


@dataclass(slots=True)
class StackState:
    stack_name: str
    plan_hash: str
    files: list[AppliedFileRecord] = field(default_factory=list)


class StateStore:
    def write(self, stack_name: str, workspace_root: str | Path, files, plan) -> Path:
        root = Path(workspace_root)
        state_dir = root / ".forgestack"
        state_dir.mkdir(parents=True, exist_ok=True)
        state_path = state_dir / "state.json"

        records = []
        for item in files:
            file_path = root / item.path
            checksum = ""
            if file_path.exists() and file_path.is_file():
                checksum = "sha256:" + hashlib.sha256(file_path.read_bytes()).hexdigest()
            records.append(AppliedFileRecord(path=item.path, checksum=checksum, plugin=item.plugin))

        plan_hash = hashlib.sha256(json.dumps(plan.to_dict(), sort_keys=True).encode("utf-8")).hexdigest()
        state = StackState(stack_name=stack_name, plan_hash=plan_hash, files=records)
        state_path.write_text(json.dumps(asdict(state), indent=2), encoding="utf-8")
        return state_path
