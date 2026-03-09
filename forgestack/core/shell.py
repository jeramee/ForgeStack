import subprocess
import os


def run_commands(commands, cwd):

    for c in commands:

        cmd = c.cmd
        workdir = os.path.join(cwd, c.cwd)

        print(f"\nRunning command: {cmd}")
        print(f"In directory: {workdir}\n")

        # Always run with shell=True on Windows for npm/npx compatibility
        subprocess.run(
            cmd,
            cwd=workdir,
            check=True,
            shell=True
        )