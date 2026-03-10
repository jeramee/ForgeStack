from pathlib import Path
import argparse

from forgestack.cli.main import _list_yaml_stems


def test_list_yaml_stems_reads_preset_names(tmp_path):
    stack_dir = tmp_path / "presets" / "stack"
    stack_dir.mkdir(parents=True)

    (stack_dir / "web-stack.yaml").write_text("kind: stack\nname: web-stack\n", encoding="utf-8")
    (stack_dir / "api-stack.yaml").write_text("kind: stack\nname: api-stack\n", encoding="utf-8")

    assert _list_yaml_stems(stack_dir) == ["api-stack", "web-stack"]