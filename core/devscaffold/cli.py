
import os
import typer
import subprocess
import socket
import shutil
from pathlib import Path

from devscaffold.core.config import load_config
from devscaffold.core.registry import load_plugins, list_available_plugins
from devscaffold.core.plan import merge_plans
from devscaffold.core.files import safe_mkdir, safe_write_text
from devscaffold.core.compose import render_compose_yaml
from devscaffold.core.shell import run_commands

app = typer.Typer(help="DevScaffold — agnostic project orchestrator")

def ensure_plugin_installed(plugin: str):
    """
    Ensure a plugin is installed. If missing, install from PyPI.
    """

    try:
        load_plugins([plugin])
        return
    except RuntimeError:
        pass

    package = f"devscaffold-{plugin}"

    typer.echo(f"Plugin '{plugin}' not installed.")
    typer.echo(f"Installing {package}...")

    subprocess.run(
        ["pip", "install", package],
        check=True
    )

    typer.echo(f"{package} installed.")

def resolve_plugin_dependencies(plugin: str):
    """
    Resolve plugin dependency chain.
    """

    resolved = []
    to_process = [plugin]

    while to_process:

        current = to_process.pop(0)

        if current in resolved:
            continue

        ensure_plugin_installed(current)

        plugin_obj = load_plugins([current])[0]

        resolved.append(current)

        deps = getattr(plugin_obj, "requires", [])

        for dep in deps:
            if dep not in resolved:
                to_process.append(dep)

    return resolved

@app.command()
def apply(config_file: str, force: bool=False, run: bool=True):

    cfg = load_config(config_file)
    name = cfg["project"]["name"]

    if os.path.exists(name) and not force:
        raise typer.BadParameter(f"Folder '{name}' exists. Use --force to overwrite")

    safe_mkdir(name, exist_ok=True)

    # Load plugins
    plugins = load_plugins(cfg.get("plugins", []))

    # Context object passed to plugins
    class Context:
        def __init__(self, cfg, root):
            self.cfg = cfg
            self.root = root

        def append_file(self, rel_path, text):
            path = os.path.join(self.root, rel_path)

            os.makedirs(os.path.dirname(path), exist_ok=True)

            existing = ""
            if os.path.exists(path):
                with open(path) as f:
                    existing = f.read()

            if text not in existing:
                with open(path, "a") as f:
                    f.write(text)

    ctx = Context(cfg, name)

    # BEFORE HOOK
    for p in plugins:
        if hasattr(p, "before_generate"):
            p.before_generate(ctx)

    # BUILD PLANS
    plans = []
    for p in plugins:
        if hasattr(p, "plan"):
            plans.append(p.plan(ctx))

    plan = merge_plans(plans)

    # WRITE FILES
    for folder in plan.folders:
        safe_mkdir(os.path.join(name, folder), exist_ok=True)

    for f in plan.files:
        safe_write_text(os.path.join(name, f.path), f.content, overwrite=True)

    # DOCKER COMPOSE
    if plan.compose:
        compose = render_compose_yaml(plan.compose)
        safe_write_text(os.path.join(name,"docker-compose.yml"), compose, overwrite=True)

    # POST GENERATE HOOK
    for p in plugins:
        if hasattr(p, "after_generate"):
            p.after_generate(ctx)

    # RUN COMMANDS
    if run:
        run_commands(plan.commands, cwd=name)

    typer.echo(f"Project created: {name}")

@app.command()
def plugin_list():
    for p in list_available_plugins():
        print(p)

@app.command()
def new(template: str, name: str, force: bool = False):
    """
    Create a project from a built-in template.

    Example:
        devscaffold new fullstack myapp
    """

    from pathlib import Path
    import shutil

    base = Path(__file__).parent
    template_file = base / "templates" / f"{template}.yaml"

    if not template_file.exists():
        typer.echo(f"Template '{template}' not found.")
        raise typer.Exit(1)

    project_dir = Path(name)

    if project_dir.exists():
        if not force:
            typer.echo(f"Folder '{name}' exists. Use --force to overwrite")
            raise typer.Exit(1)

        shutil.rmtree(project_dir)

    project_dir.mkdir()

    shutil.copy(template_file, project_dir / "project.yaml")

    typer.echo(f"Template '{template}' created project '{name}'")
    typer.echo("Running scaffold...")

    apply(str(project_dir / "project.yaml"), force=True)

@app.command()
def doctor():
    """
    Check development environment.
    """

    def exists(cmd):
        return shutil.which(cmd) is not None

    def port_free(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex(("localhost", port))
        s.close()
        return result != 0

    print("\nDevScaffold Environment Check\n")

    print("Python:", "✔" if exists("python") else "✖")
    print("Node:", "✔" if exists("node") else "✖")
    print("npm:", "✔" if exists("npm") else "✖")
    print("Docker:", "✔" if exists("docker") else "✖")

    try:
        subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Docker daemon: ✔")
    except:
        print("Docker daemon: ✖")

    print("Port 5173 free:", "✔" if port_free(5173) else "✖")
    print("Port 8000 free:", "✔" if port_free(8000) else "✖")
    print("Port 5432 free:", "✔" if port_free(5432) else "✖")

    print("\nDoctor check complete\n")

@app.command("template-list")
def template_list():
    """
    List available project templates.
    """

    from pathlib import Path

    base = Path(__file__).parent
    templates_dir = base / "templates"

    for f in templates_dir.glob("*.yaml"):
        print(f.stem)

@app.command()
def add(plugin: str):
    """
    Add a plugin to the current project.
    """

    import yaml
    from pathlib import Path

    config_file = Path("project.yaml")

    if not config_file.exists():
        typer.echo("No project.yaml found in current directory.")
        raise typer.Exit(1)

    with open(config_file) as f:
        cfg = yaml.safe_load(f)

    plugins = cfg.get("plugins", [])

    if plugin in plugins:
        typer.echo(f"Plugin '{plugin}' already enabled.")
        return

    # Auto-install plugin if missing
    deps = resolve_plugin_dependencies(plugin)

    for dep in deps:
        if dep not in plugins:
            plugins.append(dep)
    cfg["plugins"] = plugins

    with open(config_file, "w") as f:
        yaml.safe_dump(cfg, f)

    typer.echo(f"Added plugin '{plugin}'")
    typer.echo("Rebuilding project...")

    apply("project.yaml", force=True)

@app.command()
def graph():

    import yaml
    from pathlib import Path

    config_file = Path("project.yaml")

    if not config_file.exists():
        typer.echo("No project.yaml found")
        raise typer.Exit(1)

    cfg = yaml.safe_load(config_file.read_text())
    plugins = cfg.get("plugins", [])

    visited = set()

    def show(plugin, prefix=""):

        if plugin in visited:
            typer.echo(prefix + plugin + " (shared)")
            return

        visited.add(plugin)

        typer.echo(prefix + plugin)

        try:
            p = load_plugins([plugin])[0]
        except:
            return

        deps = getattr(p, "requires", [])

        for i, d in enumerate(deps):
            branch = " └ " if i == len(deps) - 1 else " ├ "
            show(d, prefix + branch)

    typer.echo("\nPlugin Dependency Graph\n")

    for p in plugins:
        show(p)

    typer.echo("")