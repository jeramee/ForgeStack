# Product Strategy

ForgeStack should be built in three strategic phases.

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

## Phase 1 — Compatibility Layer

First, ForgeStack should support the things developers already expect.

### Plugin categories

- Web app stack plugins
- Infrastructure plugins
- Observability plugins
- Dev workflow plugins

### Example v1 web stack

```yaml
plugins:
  - react
  - fastapi
  - postgres
  - redis
  - celery
```

Generated:

```text
frontend/
backend/
docker-compose.yml
.env
Makefile
```

This gives ForgeStack immediate practical value.

## Phase 2 — Ecosystem Layer

After the core is stable, ForgeStack should expand through plugins.

Targets:

- PyPI plugin discovery
- official plugin packages
- example stacks
- contributor-friendly plugin APIs

## Phase 3 — Category Creation

After trust is established, ForgeStack should pivot into spaces that are underserved.

### Data science platforms

```yaml
plugins:
  - jupyter
  - pandas
  - scikit-learn
  - postgres
  - airflow
  - fastapi
  - react_dashboard
```

Generated:

```text
notebooks/
data/
pipelines/
backend/
dashboard/
docker-compose.yml
```

### Device + backend systems

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

This is where ForgeStack becomes unique.
