# Data Science Strategy

Data science is one of the strongest future directions for ForgeStack.

## Why this matters

Data science teams constantly rebuild environments:

- Python
- Conda
- Jupyter
- ML frameworks
- databases
- orchestration tools
- serving layers

That setup is repetitive and error-prone.

ForgeStack can make it reproducible.

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

## The 5 plugin categories that matter most

### 1. Environment plugins
- python
- conda
- poetry
- pipenv
- cuda
- pytorch
- tensorflow

### 2. Notebook plugins
- jupyter
- jupyterlab
- notebook_server

### 3. Data storage plugins
- postgres
- duckdb
- minio
- s3
- parquet_store

### 4. Pipeline orchestration plugins
- airflow
- prefect
- dagster
- kedro

### 5. Model serving plugins
- fastapi
- mlflow
- bentoml
- ray

## The data science golden stack

```yaml
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

Generated:

```text
notebooks/
data/
pipelines/
models/
backend/
docker-compose.yml
```

This is more than project scaffolding.

It is **system scaffolding**.
