import subprocess
from pathlib import Path

def run_commands(commands, cwd):
    for c in commands:
        cmd = getattr(c, 'cmd', c)
        workdir = Path(cwd) / getattr(c, 'cwd', '.')
        subprocess.run(cmd, cwd=workdir, check=False)
