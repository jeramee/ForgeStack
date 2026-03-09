# Plugin System

ForgeStack is a plugin platform.

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
