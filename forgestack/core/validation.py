from __future__ import annotations

from pathlib import Path, PurePosixPath

from .models import StackModel


class ConfigValidator:
    def validate(self, stack) -> list[str]:
        errors = []
        if not stack.name:
            errors.append("Stack name is required")
        if not stack.plugins:
            errors.append("At least one plugin is required")
        for plugin in stack.plugins:
            if not plugin.name:
                errors.append("Plugin declarations must include a name")
        return errors


class GraphValidator:
    def validate(self, graph, registry) -> list[str]:
        errors = []
        for name, deps in graph.edges.items():
            for dep in deps:
                if dep not in graph.nodes and not registry.exists(dep):
                    errors.append(f"Plugin '{name}' depends on missing plugin '{dep}'")
        return errors


class PlanValidator:
    SUPPORTED_KINDS = {
        "create_dir",
        "create_file",
        "update_file",
        "append_file",
        "patch_file",
        "add_service",
        "run_command",
    }

    def validate(self, plan) -> list[str]:
        errors = []
        seen_paths = {}
        for action in plan.actions:
            if action.kind not in self.SUPPORTED_KINDS:
                errors.append(f"Unsupported action kind: {action.kind}")
            if action.path:
                if Path(action.path).is_absolute() or ".." in PurePosixPath(action.path).parts:
                    errors.append(f"Invalid path '{action.path}'")
                prior = seen_paths.get(action.path)
                compatible_file_ops = {prior, action.kind} <= {"create_file", "append_file", "patch_file", "update_file"} if prior else False
                if prior and prior != action.kind and not compatible_file_ops:
                    errors.append(f"Conflicting actions for path '{action.path}': {prior} vs {action.kind}")
                seen_paths[action.path] = action.kind
        return errors


class StackValidationError(RuntimeError):
    pass


def validate_stack(model: StackModel) -> None:
    for error in validate_stack_errors(model):
        raise StackValidationError(error)


def validate_stack_errors(model: StackModel) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_service_dependencies(model))
    errors.extend(validate_capabilities(model))
    errors.extend(validate_port_collisions(model))
    return errors


def validate_service_dependencies(model: StackModel) -> list[str]:
    errors: list[str] = []
    for service in model.services.values():
        for dep in service.depends_on:
            if dep not in model.services:
                errors.append(
                    f"Service '{service.name}' depends on unknown service '{dep}'"
                )
    return errors


def validate_capabilities(model: StackModel) -> list[str]:
    errors: list[str] = []
    if "worker:celery" in model.capabilities and "queue:redis" not in model.capabilities:
        errors.append("Celery requires a queue provider such as Redis.")
    if "backend:fastapi" in model.capabilities and "runtime:python" not in model.capabilities:
        errors.append("FastAPI requires Python runtime capability.")
    return errors


def validate_port_collisions(model: StackModel) -> list[str]:
    seen: dict[str, str] = {}
    errors: list[str] = []
    for service_name, service in model.services.items():
        for port in service.ports:
            host_port = port.split(":", 1)[0]
            prior = seen.get(host_port)
            if prior and prior != service_name:
                errors.append(
                    f"Host port '{host_port}' is used by both '{prior}' and '{service_name}'"
                )
            else:
                seen[host_port] = service_name
    return errors
