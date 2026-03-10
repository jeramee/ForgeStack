# Introduction

ForgeStack is a CLI platform for generating and managing development stacks using composable plugins.

It is best understood as:

- **Terraform for development stacks**
- **Nx for project graphs**
- **Cookiecutter for scaffolding**

That combination does not really exist today in a clean, lean form.

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

## What ForgeStack Does

ForgeStack reads a stack configuration file and generates a working development environment.

Example:

```yaml
name: ds_platform

plugins:
  - python
  - conda
  - jupyter
  - pandas
  - scikit-learn
  - postgres
  - airflow
  - mlflow
  - fastapi
```

Then:

```bash
forgestack apply ds_platform.yaml
```

Generated output may include:

```text
notebooks/
data/
pipelines/
models/
backend/
docker-compose.yml
```

## What ForgeStack Is Not

ForgeStack does **not** replace existing frameworks, CLIs, SDKs, or infrastructure systems.

It does not try to become:

- Kubernetes
- Docker
- Jupyter
- PlatformIO
- Terraform
- MLflow

Instead, ForgeStack orchestrates them.
