from __future__ import annotations

import shutil
import socket
import subprocess
from pathlib import Path
from typing import Optional

import typer

from devscaffold.core.config import load_config
from devscaffold.core.executor import DefaultExecutor
from devscaffold.core.output import ConsoleRenderer, JsonRenderer
from devscaffold.core.plan import DefaultPlanner
from devscaffold.core.registry import RegistryManager
from devscaffold.core.state import StateStore
from devscaffold.core.validation import ConfigValidator, GraphValidator, PlanValidator
from devscaffold.core.graph import GraphRenderer

app = typer.Typer(help="ForgeStack — CLI operating system for development stacks")
plugin_app = typer.Typer(help="Plugin commands")
app.add_typer(plugin_app, name="plugin")


def _build_services() -> tuple[RegistryManager, DefaultPlanner, DefaultExecutor, StateStore]:
    return RegistryManager.default(), DefaultPlanner(), DefaultExecutor(), StateStore()


def _load_and_validate_config(config_file: str):
    stack = load_config(config_file)
    errors = ConfigValidator().validate(stack)
    if errors:
        raise typer.BadParameter("\n".join(errors))
    return stack


def _build_plan(stack, registry: RegistryManager):
    planner = DefaultPlanner()
    graph, ordered_plugins, plan = planner.create_plan(stack, registry)

    graph_errors = GraphValidator().validate(graph, registry)
    if graph_errors:
        raise typer.BadParameter("\n".join(graph_errors))

    plan_errors = PlanValidator().validate(plan)
    if plan_errors:
        raise typer.BadParameter("\n".join(plan_errors))

    return graph, ordered_plugins, plan


@app.command()
def plan(
    config_file: str = typer.Argument(..., help="Path to stack YAML"),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON"),
):
    stack = _load_and_validate_config(config_file)
    registry, _planner, _executor, _state = _build_services()
    graph, ordered_plugins, plan_obj = _build_plan(stack, registry)

    if json_output:
        typer.echo(JsonRenderer().render_plan(plan_obj, stack=stack, plugins=ordered_plugins))
        return

    typer.echo(ConsoleRenderer().render_plan(plan_obj, stack=stack, plugins=ordered_plugins))


@app.command()
def apply(
    config_file: str = typer.Argument(..., help="Path to stack YAML"),
    root: Optional[str] = typer.Option(None, help="Output directory. Defaults to stack name."),
    force: bool = typer.Option(False, help="Allow writing into an existing directory."),
    skip_commands: bool = typer.Option(False, help="Skip post-generation shell commands."),
):
    stack = _load_and_validate_config(config_file)
    registry, _planner, executor, state = _build_services()
    _graph, ordered_plugins, plan_obj = _build_plan(stack, registry)

    workspace_root = Path(root or stack.name)
    if workspace_root.exists() and any(workspace_root.iterdir()) and not force:
        raise typer.BadParameter(f"Folder '{workspace_root}' exists and is not empty. Use --force to continue.")

    result = executor.apply(plan_obj, workspace_root=workspace_root, run_commands=not skip_commands)
    state.write(stack_name=stack.name, workspace_root=workspace_root, files=result.written_files, plan=plan_obj)
    typer.echo(ConsoleRenderer().render_apply_summary(stack=stack, plugins=ordered_plugins, result=result, workspace_root=workspace_root))


@app.command()
def graph(
    config_file: str = typer.Argument(..., help="Path to stack YAML"),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON"),
):
    stack = _load_and_validate_config(config_file)
    registry, _planner, _executor, _state = _build_services()
    planner = DefaultPlanner()
    graph_obj, ordered_plugins, _plan = planner.create_plan(stack, registry)

    if json_output:
        typer.echo(JsonRenderer().render_graph(graph_obj, ordered_plugins))
        return

    typer.echo(GraphRenderer().render(graph_obj, ordered_plugins))


@app.command("plugin-list")
def plugin_list():
    registry, _planner, _executor, _state = _build_services()
    for meta in registry.discover():
        typer.echo(f"{meta.name:<14} {meta.version:<8} deps={','.join(meta.requires) or '-'}")


@plugin_app.command("list")
def plugin_list_subcommand():
    plugin_list()


@app.command()
def doctor():
    def exists(cmd: str) -> bool:
        return shutil.which(cmd) is not None

    def port_free(port: int) -> bool:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex(("localhost", port))
        s.close()
        return result != 0

    typer.echo("\nForgeStack Environment Check\n")
    typer.echo(f"Python: {'✔' if exists('python') else '✖'}")
    typer.echo(f"Node: {'✔' if exists('node') else '✖'}")
    typer.echo(f"npm: {'✔' if exists('npm') else '✖'}")
    typer.echo(f"Docker: {'✔' if exists('docker') else '✖'}")

    try:
        subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        typer.echo("Docker daemon: ✔")
    except Exception:
        typer.echo("Docker daemon: ✖")

    for port in (5173, 8000, 5432, 6379):
        typer.echo(f"Port {port} free: {'✔' if port_free(port) else '✖'}")

    typer.echo("\nDoctor check complete\n")


@app.command()
def new(
    template: str = typer.Argument(..., help="Template name"),
    name: str = typer.Argument(..., help="Project directory"),
    force: bool = typer.Option(False, help="Overwrite existing directory"),
):
    template_file = Path(__file__).parent / "templates" / f"{template}.yaml"
    if not template_file.exists():
        typer.echo(f"Template '{template}' not found.")
        raise typer.Exit(1)

    project_dir = Path(name)
    if project_dir.exists():
        if not force:
            typer.echo(f"Folder '{name}' exists. Use --force to overwrite")
            raise typer.Exit(1)
        shutil.rmtree(project_dir)
    project_dir.mkdir(parents=True, exist_ok=True)

    target_config = project_dir / "project.yaml"
    target_config.write_text(template_file.read_text(encoding="utf-8"), encoding="utf-8")
    typer.echo(f"Template '{template}' created project '{name}'")
    apply(str(target_config), root=str(project_dir), force=True)


@app.command("template-list")
def template_list():
    templates_dir = Path(__file__).parent / "templates"
    for file in sorted(templates_dir.glob("*.yaml")):
        typer.echo(file.stem)


if __name__ == "__main__":
    app()
