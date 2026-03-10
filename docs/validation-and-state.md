# Validation and State

ForgeStack should validate at multiple layers.

## Documentation

- [Main README](README.md)

### Start here
- [Introduction](docs/introduction.md)
- [Docs Overview](docs/README_docs_overview.md)
- [Architecture](docs/architecture.md)
- [Roadmap](docs/roadmap.md)
- [Contributing](docs/contributing.md)

### Core platform
- [Core Engine](docs/core-engine.md)
- [Graph Engine](docs/graph-engine.md)
- [Planner](docs/planner.md)
- [Executor](docs/executor.md)
- [Validation and State](docs/validation-and-state.md)
- [Machine Readable Output](docs/machine-readable-output.md)

### Plugin and stack model
- [Plugin System](docs/plugin-system.md)
- [Stack Format](docs/stack-format.md)
- [CLI](docs/cli.md)

### Strategy and design
- [Lean Core Principles](docs/lean-core-principles.md)
- [Product Strategy](docs/product-strategy.md)
- [Data Science Strategy](docs/data-science-strategy.md)
- [Hardware Strategy](docs/hardware-strategy.md)

### Extended architecture notes
- [ForgeStack Architecture Spec](docs/forgestack_architecture_spec.md)

---

## Config validation

- stack file exists
- plugin names valid
- options conform to schema

## Registry validation

- plugin exists
- metadata is complete
- version compatibility is valid

## Graph validation

- no missing dependencies
- no cycles

## Plan validation

- no duplicate conflicting file actions
- no invalid paths
- no unsupported action kinds

Example validator:

```python
class PlanValidator:
    def validate(self, plan: Plan) -> list[str]:
        errors: list[str] = []
        seen_paths: dict[str, str] = {}

        for action in plan.actions:
            if action.path:
                prior = seen_paths.get(action.path)
                if prior and prior != action.kind:
                    errors.append(
                        f"Conflicting actions for path '{action.path}': {prior} vs {action.kind}"
                    )
                seen_paths[action.path] = action.kind

        return errors
```

## State design

Recommended state file:

```text
.forgestack/state.json
```

Example:

```json
{
  "stack_name": "my_stack",
  "plan_hash": "abc123",
  "files": [
    {
      "path": "backend/main.py",
      "checksum": "sha256:...",
      "plugin": "fastapi"
    }
  ]
}
```

This unlocks:

- diff
- upgrade
- drift detection
- plugin ownership of generated files
