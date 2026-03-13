# ForgeStack

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active%20development-orange)

ForgeStack is a modular platform for generating applications and workflow systems from composable presets and plugins.

Its current active CLI is **`devmake`**.

Instead of manually wiring frontends, backends, databases, queues, workers, and infrastructure, ForgeStack generates a connected starter system from a small declarative project definition.

**TL;DR:**  
ForgeStack can generate a connected full-stack starter app from a project definition in **one command**:

`devmake apply projects/MyApp.yaml`

Build the project definition once. Generate the full stack whenever you want.

---

## What ForgeStack Is

ForgeStack is built around a small object model:

- **stack** = technical preset
- **app** = product or archetype preset
- **project** = concrete instance using a stack and app
- **output** = rendered filesystem result

This keeps technical composition, product intent, project identity, and generated artifacts separate.

That separation is a core design rule of the platform.

---

## Current Status

ForgeStack has moved beyond a basic scaffold demo into a preset-driven generation system that can produce a runnable connected starter app.

Current working generated full-stack slice includes:

- React frontend
- FastAPI backend
- PostgreSQL
- Redis
- Celery worker
- Docker build flow
- backend config endpoint
- task queue trigger flow

Implemented v1.5 lanes now also include:

- SQLite-backed local workflow apps
- technician console / mobile-responsive operational UI
- Jupyter workspace lane
- Voilà notebook-view bridge
- structured workflow / Kedro scaffold
- Arduino-first device bridge scaffold

ForgeStack is still under active development, but the current direction is now centered on:

- `presets/`
- `projects/`
- `output/`
- dependency-aware plugin planning
- canonical internal templates
- generated application skeletons

---

## Canonical Repository Model (Representative Example)

```text
presets/
  stack/
    web-stack.yaml
    api-stack.yaml
    local-workflow-stack.yaml
    data-workbench-stack.yaml
    notebook-view-stack.yaml
    structured-workflow-stack.yaml
    device-bridge-stack.yaml
    ml-stack.yaml

  app/
    finance-dashboard.yaml
    technician-console.yaml
    data-workbench.yaml
    notebook-view.yaml
    pipeline-workbench.yaml
    device-ops-console.yaml

projects/
  MyApp.yaml
  LocalWorkflowApp.yaml
  TechnicianConsoleApp.yaml
  DataWorkbenchApp.yaml
  NotebookViewApp.yaml
  PipelineWorkbenchApp.yaml
  DeviceOpsConsoleApp.yaml

output/
  MyApp/

forgestack/
  templates/
```

This is a representative repository shape, not a complete live inventory of every current preset.

### Meaning

- `presets/stack/` contains reusable technical presets
- `presets/app/` contains reusable product or archetype presets
- `projects/` contains concrete project definitions
- `output/` contains generated results
- `forgestack/templates/` contains internal render templates, not user-facing presets

---

## Current CLI

ForgeStack currently uses **`devmake`** as the active CLI.

Supported command family:

```powershell
devmake plugins
devmake presets list
devmake graph projects/MyApp.yaml
devmake plan projects/MyApp.yaml
devmake apply projects/MyApp.yaml
devmake create project MyApp --stack web-stack --app finance-dashboard
```

### Recommended near-term flow

```powershell
devmake presets list
devmake create project MyApp --stack web-stack --app finance-dashboard
devmake plan projects/MyApp.yaml
devmake apply projects/MyApp.yaml
```

---

## Quick Start

### 1. Create and activate a virtual environment

```powershell
python.exe -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install ForgeStack

```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
```

### 3. List available presets

```powershell
devmake presets list
```

### 4. Create a project

```powershell
devmake create project MyApp --stack web-stack --app finance-dashboard
```

### 5. Preview the dependency graph

```powershell
devmake graph projects/MyApp.yaml
```

### 6. Preview the execution plan

```powershell
devmake plan projects/MyApp.yaml
```

### 7. Generate the project

```powershell
devmake apply projects/MyApp.yaml
```

### 8. Run the generated stack

```powershell
cd output\MyApp
docker compose up --build
```

---

## Example Project Definition

Example `projects/MyApp.yaml`:

```yaml
kind: project
name: MyApp
uses:
  stack: web-stack
  app: finance-dashboard
overrides: {}
```

This project definition points to reusable presets instead of mixing all concerns into one document.

---

## Generated Output Direction

ForgeStack now aims to generate more than placeholder files.

A generated full-stack starter app may include:

```text
output/MyApp/
  backend/
    main.py
    app_config.py
    celery_app.py
    tasks.py
    requirements.txt
    Dockerfile

  frontend/
    package.json
    index.html
    Dockerfile
    src/
      main.jsx
      App.jsx

  docker/
    postgres.yml
    redis.yml
    celery.yml

  docker-compose.yml
  README.md
  .env.example
  .gitignore
```

The current generated application skeleton is moving toward a true vertical slice:

- frontend calls backend
- backend exposes real endpoints
- backend returns project config
- backend queues a background task
- frontend can display results from that flow

---

## Core Design Direction

ForgeStack is no longer centered on a single mixed stack file.

It is now centered on a declarative model with clean separation between:

- reusable technical composition
- reusable app/archetype composition
- concrete project identity
- generated filesystem output

This improves:

- clarity
- reusability
- CLI readability
- long-term scalability
- future tooling expansion

---

## Why ForgeStack

Modern systems require many pieces to be wired together correctly:

- frontend frameworks
- backend frameworks
- databases
- queues
- workers
- environment settings
- infrastructure glue
- service dependencies

ForgeStack automates that wiring through a dependency-aware plugin system.

The goal is not just to scaffold files, but to generate a connected development starting point that matches a chosen stack and app shape.

---

## Current Product Direction

ForgeStack should remain general enough for broad business and workflow applications, while developing a stronger near-term niche in:

- data science tooling
- technician tooling
- internal workflow systems

Longer term, the same platform may support:

- operator panels
- lightweight mobile-responsive frontends
- local-processing tools
- hub-oriented application patterns
- document and workflow systems
- additional tool families under the broader ForgeStack platform

Those future lanes are important, but the current priority is keeping the core model and generation path stable.

---

## Platform and Tooling Direction

ForgeStack is the **platform**.

`devmake` is the current active **tool** inside that platform.

Planned future ForgeStack tool families may include:

- `devdata`
- `devview`
- `devhub`
- `devai`
- `devpkg`

For now, development is centered on the core ForgeStack repository and the `devmake` generation path.

---

## Documentation

### Start here
- [Introduction](docs/introduction.md)
- [Docs Overview](docs/README_docs_overview.md)
- [Current Architecture](docs/current-architecture.md)
- [CLI](docs/cli.md)
- [Roadmap](docs/roadmap.md)

### Core model
- [Object Model](docs/object-model.md)
- [Presets and Projects](docs/presets-and-projects.md)
- [Plugin System](docs/plugin-system.md)

### Engine internals
- [Core Engine](docs/core-engine.md)
- [Graph Engine](docs/graph-engine.md)
- [Planner](docs/planner.md)
- [Executor](docs/executor.md)
- [Validation and State](docs/validation-and-state.md)
- [Machine Readable Output](docs/machine-readable-output.md)

### Strategy and design
- [Lean Core Principles](docs/lean-core-principles.md)
- [Product Strategy](docs/product-strategy.md)
- [Data Science Strategy](docs/data-science-strategy.md)
- [Hardware Strategy](docs/hardware-strategy.md)
- [Platform Tools](docs/platform-tools.md)

### Extended design notes
- [ForgeStack Architecture Spec](docs/forgestack_architecture_spec.md)

---

## Contributing

ForgeStack is still evolving, and contributions should preserve a few core rules:

- keep the core small
- keep behavior in plugins where possible
- preserve plan-before-apply
- treat the dependency graph as a first-class primitive
- keep the object model clean:
  - stack
  - app
  - project
  - output

See [Contributing](docs/contributing.md).

---

## License

MIT License
