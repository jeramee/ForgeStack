# Lean Core Principles

ForgeStack should remain efficient and maintainable by following strict architectural rules.

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

## Core rule

Treat **all external systems as plugins**.

That includes:

- Docker
- Kubernetes
- cloud providers
- ML frameworks
- hardware toolchains

## Plugin isolation rule

Plugins may depend on heavy libraries.

Examples:

- `forgestack-plugin-kubernetes` → kubernetes SDK
- `forgestack-plugin-pytorch` → torch
- `forgestack-plugin-arduino` → platformio or arduino-cli wrappers

The core must never import those dependencies.

## Correct pattern

Good:

```python
class KubernetesPlugin(Plugin):
    def plan(self, ctx):
        ctx.create_file("k8s/deployment.yaml", "...")
```

Bad:

```python
# core package imports kubernetes and calls cluster APIs directly
```

## Optional tool execution

If a plugin wants to run commands like:

- `kubectl apply`
- `terraform apply`
- `platformio run`

those should be optional actions, not core requirements.

Users should be able to disable command execution:

```bash
forgestack apply --skip-commands
```

## Dependency philosophy

Keep core dependencies minimal:

- PyYAML
- rich (optional)
- pydantic or jsonschema (optional)
- networkx (optional)

No heavyweight platform dependencies in the core.
