# ForgeStack

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-development-orange)

ForgeStack is a modular project generation platform that builds complete application stacks from composable plugins.

Instead of manually wiring APIs, frontends, databases, queues, and infrastructure, ForgeStack generates a fully wired development stack from a simple configuration file.

ForgeStack acts as a stack factory for modern development environments.

**TL;DR:**  
Once ForgeStack is configured, you can generate a wired full-stack project with a single command. Frontend, backend, databases, queues, and infrastructure are created through a dependency-aware plugin system.

---

## Documentation

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

## Why ForgeStack

Modern projects require wiring many systems together:

- backend frameworks
- frontend frameworks
- databases
- workers
- Docker
- environment variables
- service dependencies

ForgeStack automates this setup.

A single configuration file can generate:

- React frontend
- FastAPI backend
- PostgreSQL database
- Redis queue
- Celery workers
- Docker infrastructure

All components are connected through a dependency-aware plan.

---

## Quick Start

### 1. Create a virtual environment

```powershell
python.exe -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install ForgeStack

```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
```

### 3. Inspect available plugins

```powershell
devmake plugins
```

### 4. View a dependency graph

```powershell
devmake graph stack.yaml
```

### 5. Preview the execution plan

```powershell
devmake plan stack.yaml
```

### 6. Generate the stack

```powershell
devmake apply stack.yaml
```

---

## Example Stack File

Example `stack.yaml`:

```yaml
plugins:
  - react
  - fastapi
  - postgres
```

Run:

```powershell
devmake apply stack.yaml
```

---

## CLI Commands

```powershell
devmake plugins
devmake graph stack.yaml
devmake plan stack.yaml
devmake apply stack.yaml
```

---

## What ForgeStack Does

ForgeStack currently follows this execution flow:

```text
stack.yaml
  ↓
plugin registry
  ↓
dependency graph
  ↓
execution waves
  ↓
plan generation
  ↓
apply executor
```

This means ForgeStack can:

- discover installed plugins
- resolve plugin dependencies
- build a dependency graph
- execute independent plugins in parallel waves
- generate an execution plan
- apply that plan to produce project files

---

## Current Example Output

### Plugin discovery

```text
Installed Plugins:

- fastapi
- postgres
- python
- react
- redis
```

### Dependency graph

```text
Dependency Graph:
react -> []
fastapi -> ['python']
python -> []
postgres -> []
```

### Execution plan

```text
Execution Plan:
- {'type': 'create_file', 'path': 'docker/postgres.yml', 'template': 'postgres_docker', 'content': None}
- {'type': 'create_file', 'path': 'backend/requirements.txt', 'template': 'python_requirements', 'content': None}
- {'type': 'create_file', 'path': 'frontend/package.json', 'template': 'react_package', 'content': None}
- {'type': 'create_file', 'path': 'backend/main.py', 'template': 'fastapi_main', 'content': None}
```

---

## Repository Structure

```text
ForgeStack/
├── docs/
├── examples/
├── forgestack/
│   ├── cli/
│   ├── core/
│   ├── plugins/
│   └── templates/
├── backend/
├── docker/
├── frontend/
├── pyproject.toml
├── README.md
├── requirements.txt
├── run_cli.py
└── stack.yaml
```

---

## Plugin System

Plugins can:

- generate files
- declare dependencies
- contribute stack capabilities
- participate in planning and apply steps

Example dependency declaration:

```python
class FastAPIPlugin(Plugin):
    def __init__(self):
        super().__init__("fastapi", ["python"])
```

ForgeStack resolves dependencies automatically.

---

## Design Direction

ForgeStack is moving from a basic scaffold tool toward a true stack composition platform.

That means:

- plugins describe capabilities and requirements
- the system builds a dependency-aware execution model
- generation becomes deterministic and easier to validate
- future renderers can target multiple output styles

See:

- [Architecture](docs/architecture.md)
- [Core Engine](docs/core-engine.md)
- [Plugin System](docs/plugin-system.md)
- [Lean Core Principles](docs/lean-core-principles.md)

---

## Roadmap

Planned improvements include:

- richer stack composition model
- PyPI plugin discovery
- plugin marketplace
- graphical stack builder
- CI/CD integrations
- infrastructure modules
- cleaner plan rendering
- improved apply execution
- expanded plugin ecosystem

For more detail, see [Roadmap](docs/roadmap.md).

---

## Contributing

See [Contributing](docs/contributing.md).

---

## License

MIT License
