# Architecture

ForgeStack uses a thin-core, plugin-driven architecture.

## Core pipeline

```text
CLI
↓
Config Loader
↓
Plugin Registry
↓
Dependency Resolver
↓
Dependency Graph
↓
Planner
↓
Executor
↓
State Store
↓
Output Renderer
```

## Core responsibilities

The core should only do a small set of things:

- parse stack configuration
- discover plugins
- validate metadata
- resolve dependencies
- build a dependency graph
- generate a plan
- execute actions
- store state
- render human and machine-readable output

## What belongs in plugins

All domain-specific complexity belongs in plugins:

- React
- FastAPI
- Postgres
- Docker
- Kubernetes
- AWS
- Jupyter
- MLflow
- Airflow
- Arduino
- PlatformIO

## Lean core target

The core should stay around **5–8k lines** total.

That means:

- no cloud SDKs in core
- no ML frameworks in core
- no hardware SDKs in core
- no Kubernetes dependency in core

ForgeStack core understands only:

- plugins
- actions
- graph
- plan
- execution
- validation
- state
