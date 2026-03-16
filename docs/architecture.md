<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** [Prev: Current Architecture](current-architecture.md) | [Next: CLI](cli.md)  
> **Related:** [Object Model](object-model.md)

# Architecture

This document describes the **current implemented architecture** of ForgeStack.

It should be read as the main architecture document for the current project state, not as an older stack-only description and not as a broad future-only wishlist.

ForgeStack is a modular platform for generating applications and workflow systems from composable presets and plugins.

Its current active CLI is **`devmake`**.

---

## Architectural Summary

ForgeStack is now centered on a declarative object model with clean separation between:

- **stack** = reusable technical preset
- **app** = reusable product or archetype preset
- **project** = concrete instance
- **output** = rendered filesystem result

This separation is one of the main architectural rules of the platform.

ForgeStack is no longer centered on one mixed configuration file that tries to act as preset, project, override object, and output definition at the same time.

---

## Current Repository Model

The current recommended repository shape is:

```text
presets/
  stack/
    api-stack.yaml
    web-stack.yaml
    ml-stack.yaml

  app/
    finance-dashboard.yaml
    datascience-dashboard.yaml
    simple-dashboard.yaml
    ai-dashboard.yaml

projects/
  MyApp.yaml

output/
  MyApp/

forgestack/
  templates/
```

### Meaning

- `presets/stack/` contains reusable technical presets
- `presets/app/` contains reusable product presets
- `projects/` contains concrete project definitions
- `output/` contains generated filesystem results
- `forgestack/templates/` contains internal render templates

`forgestack/templates/` is not a user-facing preset area.

---

## Current CLI Surface

ForgeStack currently uses **`devmake`** as the active CLI.

The current command family is:

```powershell
devmake plugins
devmake presets list
devmake create project MyApp --stack web-stack --app finance-dashboard
devmake graph projects/MyApp.yaml
devmake plan projects/MyApp.yaml
devmake apply projects/MyApp.yaml
```

The architecture should support this flow clearly and explicitly.

---

## High-Level Execution Flow

The current generation path looks like this:

```text
project file
  ->
load YAML
  ->
resolve stack/app presets
  ->
build render context
  ->
discover plugins
  ->
build dependency graph
  ->
create execution plan
  ->
apply plan into output/
```

In the current repo, this public flow is anchored to `cli/main.py`, `stack_loader.py`, `preset_resolver.py`, `registry.py`, `planner.py`, and `plan_executor.py`.

This means ForgeStack now has a real resolution step before planning and apply.

It is no longer just "read plugin names from one file and render a few templates."

---

## Canonical Objects

## 1. Stack

A **stack** is a reusable technical preset.

It defines the reusable technical shape of a generated system.

A stack may include:

- plugin composition
- service profile
- technical defaults
- framework and service selection
- capability defaults

A stack should not own:

- final project identity
- product branding
- instance-specific overrides
- output folder meaning

---

## 2. App

An **app** is a reusable product or archetype preset.

It defines product-facing or workflow-facing intent.

An app may include:

- feature modules
- UX shape
- workflow shape
- domain or archetype intent
- default stack affinity

An app should not own:

- low-level technical wiring
- plugin dependency mechanics
- concrete project identity
- internal rendering details

---

## 3. Project

A **project** is a concrete instantiated object.

It chooses a stack preset and an app preset, assigns a real project name, and optionally adds overrides.

Example:

```yaml
kind: project
name: MyApp
uses:
  stack: web-stack
  app: finance-dashboard
overrides: {}
```

A project is the main input to the current `graph`, `plan`, and `apply` commands.

---

## 4. Output

**Output** is the rendered filesystem result of applying a project.

Example:

```text
output/MyApp/
```

Output is a result, not part of the reusable preset model.

It may contain generated:

- frontend files
- backend files
- worker files
- Docker files
- environment files
- project README files

---

## Resolution Pipeline

ForgeStack uses a layered resolution model.

### Layers

1. **Raw document**
   - the project file the user passes in

2. **Resolved document**
   - the normalized project after referenced stack/app presets are loaded and merged

3. **Render context**
   - the structured context passed into plugins and templates

### Why this matters

This architecture allows generation to stay declarative while still letting templates and plugins see:

- project identity
- resolved stack info
- resolved app info
- values and overrides
- features
- plugin set

That is one of the key shifts from the older stack-only model.

---

## Render Context

The current architecture builds a render context that includes values such as:

- raw project document
- effective resolved document
- project name
- stack object
- app object
- values
- plugin list
- feature list
- feature booleans

This means template rendering is now **project-model aware**, not just plugin-name aware.

That is why generated files can now include:

- project name
- stack name
- app name
- feature flags
- resolved service settings

---

## Plugin Architecture

ForgeStack still follows a **small core, plugin-driven behavior** model.

### Core responsibilities
- configuration loading
- preset resolution
- plugin discovery
- dependency resolution
- graph building
- plan construction
- plan execution

### Plugin responsibilities
Plugins declare what should be generated.

Typical plugin contributions include:

- create file actions
- template selection
- dependency declarations

The core rule remains:

**Core coordinates. Plugins declare. Executor applies.**

---

## Dependency Graph

The dependency graph remains a first-class primitive in the architecture.

### Why it matters
The graph determines:

- ordering
- execution waves
- dependency-aware planning
- graph visualization
- diagnostic clarity

### Current path

```text
requested or resolved plugins
  ->
dependency expansion
  ->
graph build
  ->
topological ordering
  ->
plugin planning hooks
  ->
plan actions
```

This graph-first behavior is one of the defining parts of ForgeStack.

---

## Planner and Executor

ForgeStack follows a **plan-before-apply** architecture.

### Planner
The planner:

- resolves dependency order
- runs plugin planning hooks
- collects actions
- validates the plan

### Executor
The executor:

- applies plan actions
- writes generated files
- produces the output tree

This separation improves:

- safety
- clarity
- reproducibility
- future testability
- future machine-readable output

---

## Template System

ForgeStack uses internal templates under:

```text
forgestack/templates/
```

These are implementation details, not user-facing presets.

Current template behavior includes:

- canonical template IDs
- alias resolution where needed
- context-driven rendering
- feature-aware rendering

The user-facing schema and CLI should stay above this layer.

That means users interact with:

- stack presets
- app presets
- project objects

and the engine internally maps those to plugins, plans, and templates.

---

## Current Generated Output Direction

ForgeStack has already moved into generating a much fuller starter system.

A generated output may include:

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

This is much closer to a real generated application skeleton than the earlier demo-stage output.

---

## Current Runtime Milestone

ForgeStack has crossed an important line:

### From
- declarative preset-driven scaffolding

### To
- preset-driven generation of a runnable connected full-stack starter app

The generated system now includes:

- React frontend
- FastAPI backend
- Redis
- Postgres
- Celery
- Docker build flow

And it has been moving toward a connected vertical slice where:

- frontend calls backend
- backend exposes real endpoints
- backend returns structured config
- backend queues background work
- frontend displays the result of that flow

That is the most important current runtime milestone.

---

## Near-Term Priorities

The main near-term architectural priorities are:

1. keep the stack/app/project/output model stable
2. keep `presets/`, `projects/`, and `output/` cleanly separated
3. keep the CLI aligned with explicit project creation
4. strengthen the generated application skeleton path
5. harden tests around generated output and runtime behavior
6. reduce ambiguity between user-facing presets and internal templates

These priorities are what keep the project from drifting backward into mixed definitions and older patterns.

---

## Relationship to Future Expansion

ForgeStack may later expand into:

- stronger data-science tooling
- technician tooling
- partial frontends
- local-processing systems
- SQLite-backed lightweight systems
- hub-oriented application patterns
- broader platform tool families

But those future lanes should be layered on top of the same architecture rather than used to redefine it prematurely.

That is why the object model and current resolution path matter so much.

---

## Design Rule

The architecture should remain aligned with the canonical object model and the current `devmake` workflow.

That means:

- stack remains reusable technical composition
- app remains reusable product/archetype composition
- project remains the concrete instance
- output remains the generated result

ForgeStack should continue growing from this structure instead of slipping back into mixed, hard-to-scale configuration patterns.

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** [Prev: Current Architecture](current-architecture.md) | [Next: CLI](cli.md)  
**Related:** [Object Model](object-model.md)