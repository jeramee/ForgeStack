# Plugin System

ForgeStack is a plugin platform.

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

## Stable v1 extension points

These should be treated as stable interfaces in ForgeStack v1:

- `Plugin`
- `PluginMetadata`
- `PluginContext`
- `PlanAction`
- `Plan`
- `PluginRegistry`
- `DependencyResolver`
- `Planner`
- `Executor`

## Plugin responsibilities

A plugin may:

- generate files
- patch files
- add services
- register commands
- contribute notes
- declare dependencies

## Plugin contract

Plugins should declare intent, not execute side effects directly.

```python
class Plugin:
    metadata: PluginMetadata

    def before_generate(self, ctx):
        pass

    def plan(self, ctx):
        pass

    def after_generate(self, ctx):
        pass
```

## Official plugin families

### Compatibility layer plugins
- react
- vue
- nextjs
- fastapi
- django
- node
- postgres
- redis
- celery
- nginx
- docker

### Infrastructure plugins
- kubernetes
- terraform
- aws
- gcp
- azure
- s3

### Observability plugins
- grafana
- prometheus
- loki
- opentelemetry
- sentry

### Dev workflow plugins
- pytest
- precommit
- ruff
- black
- github_actions
- gitlab_ci

### Data science plugins
- python
- conda
- poetry
- jupyter
- pandas
- scikit-learn
- pytorch
- tensorflow
- duckdb
- minio
- airflow
- prefect
- dagster
- kedro
- mlflow
- bentoml
- ray

### Hardware plugins
- arduino
- platformio
- esp32
- mqtt
- grafana
