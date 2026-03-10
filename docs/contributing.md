# Contributing

ForgeStack should be easy to extend and safe to maintain.

## Contribution rules

1. Keep the core small.
2. Prefer plugins over core feature growth.
3. Avoid heavy dependencies in the core.
4. Preserve the planner/executor split.
5. Treat the graph as a first-class primitive.
6. Add docs for all new extension points.
7. Add tests for all new core behaviors.

## Architectural rule

Before adding something to the core, ask:

- Can this be a plugin?
- Can this be represented as a plan action?
- Does the core need to know about this system at all?

If the answer is no, keep it out of the core.

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