# Introduction

ForgeStack is a CLI platform for generating and managing development stacks using composable plugins.

It is best understood as:

- **Terraform for development stacks**
- **Nx for project graphs**
- **Cookiecutter for scaffolding**

That combination does not really exist today in a clean, lean form.

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
