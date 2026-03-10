# Roadmap

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

## ForgeStack v1

Core platform features:

- CLI renamed to `forgestack`
- plugin interface stabilized
- dependency graph
- plan engine
- executor
- PyPI plugin discovery
- official core plugins
- example stacks
- JSON plan output
- minimal state store

## ForgeStack v1.5

Lifecycle and ecosystem features:

- `forgestack diff`
- `forgestack validate`
- `forgestack upgrade`
- `forgestack new plugin`
- plugin compatibility checks
- improved state handling
- richer machine-readable outputs

## ForgeStack v2

Category expansion:

- hardware toolchain plugins
- Arduino / PlatformIO support
- device + backend example stacks
- broader data science platform presets
- optional GUI only after CLI adoption
