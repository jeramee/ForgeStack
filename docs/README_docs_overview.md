# ForgeStack Documentation Overview

This documentation set reflects the current ForgeStack direction:

- **Terraform for development stacks**
- **Nx for project graphs**
- **Cookiecutter for scaffolding**

ForgeStack is a **lean orchestration core** with a **plugin ecosystem**.

The core is responsible for:

- config loading
- plugin discovery
- dependency resolution
- graph construction
- planning
- execution
- validation
- state

Everything else is a plugin:

- web frameworks
- databases
- cloud integrations
- observability
- data science tools
- hardware toolchains

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

## Strategic Direction

ForgeStack follows a three-phase product strategy:

1. **Compatibility Layer**  
   Match the developer experience people already expect from web and infra tooling.

2. **Ecosystem Layer**  
   Expand through official and third-party plugins.

3. **Category Creation**  
   Pivot hard into:
   - Data science platform scaffolding
   - Device + backend scaffolding

## Golden Rule

ForgeStack should never become a platform that *runs everything*.

ForgeStack should become a system that *wires everything*.
