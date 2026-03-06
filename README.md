# ForgeStack

![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-development-orange)


ForgeStack is a modular project generation platform that builds complete application stacks from composable plugins.

Instead of manually wiring APIs, frontends, databases, queues, and infrastructure, ForgeStack generates a fully wired development stack from a simple configuration file.

ForgeStack acts as a stack factory for modern development environments.

**TL;DR:** 

Once ForgeStack is configured, you can generate a fully wired, production-ready full-stack project with a single command. Frontend, backend, databases, workers, and infrastructure are created and connected automatically!

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

React frontend
FastAPI backend
PostgreSQL database
Redis queue
Celery workers
Docker infrastructure

All components are automatically connected.

---

## Quick Start

Create a virtual environment.

```
python -m venv .venv
source .venv/bin/activate
```

Install ForgeStack and built-in plugins.

```
pip install -e core
pip install -e plugins/react
pip install -e plugins/fastapi
pip install -e plugins/postgres

Generate a project.

devscaffold apply examples/project.yaml

Start the generated stack.

cd ai-dashboard
docker compose up
```

---

## Example Configuration

ForgeStack builds projects from a YAML configuration file.

project:
  name: my-ai-app

plugins:
  - react
  - fastapi
  - postgres

Run:

devscaffold apply project.yaml

---

## CLI Commands

```
devscaffold new fullstack myapp
devscaffold apply project.yaml
devscaffold plugin-list
devscaffold template-list
devscaffold add redis
devscaffold add celery
devscaffold graph
devscaffold doctor
```

---

## Architecture

CLI
 ↓
Plugin Registry
 ↓
Generator Engine
 ↓
Merged Plan
 ↓
Generated Project

Plugins support lifecycle hooks:

- before_generate
- plan
- after_generate

---

## Plugin System

Plugins can:

- generate files
- modify configuration
- inject infrastructure
- declare dependencies

Example dependency declaration:

class CeleryPlugin:

    requires = ["redis"]

ForgeStack resolves dependencies automatically.

---

## Repository Structure

```
forgestack/
    core/
    plugins/
    examples/
    ai-dashboard/
    ai-startup/
    README.md
    LICENSE
```

---

## Roadmap

Future improvements:

- plugin/template marketplace
- PyPI plugin discovery
- graphical stack builder
- CI/CD integrations
- infrastructure modules

---

## License

MIT License
