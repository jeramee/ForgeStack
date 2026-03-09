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
