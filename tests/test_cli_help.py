import sys

import pytest

from forgestack.cli.main import main


def test_cli_help_runs(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["devmake", "--help"])

    with pytest.raises(SystemExit) as excinfo:
        main()

    assert excinfo.value.code == 0

    out = capsys.readouterr().out
    assert "usage: devmake" in out
    assert "plan" in out
    assert "apply" in out
    assert "create" in out