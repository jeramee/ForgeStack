# Hardware and Device Strategy

ForgeStack should eventually support device + backend scaffolding.

## Why this is interesting

Very few developer tools scaffold end-to-end systems that include:

- firmware
- messaging
- backend APIs
- storage
- monitoring

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

## Example stack

```yaml
plugins:
  - arduino
  - mqtt
  - fastapi
  - postgres
  - grafana
```

Generated:

```text
firmware/
edge/
backend/
dashboard/
docker-compose.yml
```

## Design rule

ForgeStack should not become an embedded framework.

It should orchestrate hardware toolchains the same way it orchestrates web and DS stacks.

That means:

- Arduino is a plugin
- PlatformIO is a plugin
- MQTT is a plugin
- Grafana is a plugin

The core only wires the system together.
