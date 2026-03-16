<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** [Next: Docs Overview](README_docs_overview.md)  
> **Related:** [Object Model](object-model.md)

# Introduction

ForgeStack is a modular platform for generating applications and workflow systems from composable presets and plugins.

Its current active CLI is **`devmake`**.

Rather than manually wiring a frontend, backend, database, queue, worker system, and surrounding configuration by hand, ForgeStack allows those pieces to be generated from a small declarative project definition.

---

## What ForgeStack Is

ForgeStack is not just a file scaffolder.

It is a generation platform built around a clean object model:

- **stack** = technical preset
- **app** = product or archetype preset
- **project** = concrete instance
- **output** = rendered filesystem result

This keeps technical composition, product intent, project identity, and generated artifacts separate.

That separation makes the system easier to understand, easier to scale, and easier to extend.

---

## Current Active Tool

ForgeStack is the platform.

**`devmake`** is the current active CLI tool inside that platform.

Current command family includes:

```powershell
devmake plugins
devmake presets list
devmake create project MyApp --stack web-stack --app finance-dashboard
devmake graph projects/MyApp.yaml
devmake plan projects/MyApp.yaml
devmake apply projects/MyApp.yaml
```

This is the current working path and should be treated as the main user-facing workflow.

---

## What ForgeStack Does Today

ForgeStack currently generates connected starter systems using:

- reusable technical presets
- reusable app presets
- dependency-aware plugins
- canonical internal templates
- plan-before-apply execution

The current working generated stack includes:

- React frontend
- FastAPI backend
- PostgreSQL
- Redis
- Celery
- Docker build flow

The generated application skeleton is moving beyond placeholder output toward a real vertical slice, including:

- frontend calling backend
- backend exposing real endpoints
- backend returning project config
- backend queueing background work
- frontend displaying the result of that flow

---

## Canonical Model

ForgeStack now follows a clearer repository and object model than the older stack-only approach.

### Repository shape

```text
presets/
  stack/
  app/

projects/

output/

forgestack/
  templates/
```

### Meaning

- `presets/stack/` contains reusable technical presets
- `presets/app/` contains reusable product or archetype presets
- `projects/` contains concrete project instances
- `output/` contains generated artifacts
- `forgestack/templates/` contains internal render templates

This helps ForgeStack avoid mixing:
- reusable definitions
- concrete instances
- generated files

---

## Example Project Flow

Create a project:

```powershell
devmake create project MyApp --stack web-stack --app finance-dashboard
```

This creates a project definition such as:

```yaml
kind: project
name: MyApp
uses:
  stack: web-stack
  app: finance-dashboard
overrides: {}
```

Then inspect and generate it:

```powershell
devmake graph projects/MyApp.yaml
devmake plan projects/MyApp.yaml
devmake apply projects/MyApp.yaml
```

Then run the generated system:

```powershell
cd output\MyApp
docker compose up --build
```

---

## What ForgeStack Is Not

ForgeStack does **not** try to replace the major frameworks and systems it works with.

It is not trying to become:

- React
- FastAPI
- PostgreSQL
- Redis
- Celery
- Docker
- Jupyter
- Kedro
- PlatformIO

Instead, ForgeStack is meant to **wire systems together**, not replace them.

That is one of its central design rules.

---

## Current Product Direction

ForgeStack should remain general enough for broad business and workflow applications.

At the same time, its strongest near-term wedge is likely in:

- data science tooling
- technician tooling
- internal workflow systems

Longer term, the same platform may support:

- operator panels
- lightweight mobile-responsive frontends
- local-processing tools
- hub-oriented application patterns
- document and workflow systems
- broader ForgeStack tool families

Those future lanes are important, but they should be built on top of the same core model rather than used to redefine it.

---

## Design Principle

The core rule of ForgeStack is:

**Core coordinates. Plugins declare. Executor applies.**

That means:

- the core stays small
- plugins describe behavior
- plans are generated before execution
- output is deterministic and easier to validate

This keeps the platform maintainable while still allowing it to grow.

---

## Where to Go Next

If you are new to ForgeStack, read these next:

- [Docs Overview](README_docs_overview.md)
- [CLI](cli.md)
- [Object Model](object-model.md)
- [Presets and Projects](presets-and-projects.md)
- [Current Architecture](current-architecture.md)

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** [Next: Docs Overview](README_docs_overview.md)  
**Related:** [Object Model](object-model.md)