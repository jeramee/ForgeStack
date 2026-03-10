# Machine Readable Output

ForgeStack should support machine-readable outputs early.

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

## JSON plan output

```bash
forgestack plan --json
```

Example:

```json
{
  "actions": [
    {
      "kind": "create_dir",
      "path": "backend",
      "description": "Create backend app directory"
    },
    {
      "kind": "create_file",
      "path": "backend/main.py",
      "description": "Create FastAPI entrypoint"
    }
  ],
  "warnings": [],
  "diagnostics": []
}
```

## Why this matters

Machine-readable outputs enable:

- CI checks
- editor integrations
- future GUI work
- policy engines
- testing
