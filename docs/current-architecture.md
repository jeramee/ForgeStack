# Current Architecture

This document describes the **current implemented direction** of ForgeStack.

It is not a broad future architecture wish list and it is not the older stack-only model. Its purpose is to explain the architecture that the project is actively converging on now.

ForgeStack is a modular platform for generating applications and workflow systems from composable presets and plugins.

Its current active CLI is **`devmake`**.

---

## What This Document Covers

This document focuses on the current architectural direction for:

- the canonical object model
- preset and project resolution
- plugin planning
- plan execution
- template rendering
- generated output structure
- the current generated application skeleton path

It should be read as the bridge between the design-lock documents and the actual implementation path.

---

## Canonical Model

The current architecture is built around four main objects:

- **stack**
- **app**
- **project**
- **output**

### Meaning

- **stack** = reusable technical preset
- **app** = reusable product or archetype preset
- **project** = concrete instance using a stack and app
- **output** = rendered filesystem result

This separation is now a core architectural rule.

ForgeStack is no longer centered on one mixed stack file that tries to act as preset, project, and override object at the same time.

---

## Repository Model

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

The current CLI is **`devmake`**.

The current command family is:

```powershell
devmake plugins
devmake presets list
devmake create project MyApp --stack web-stack --app finance-dashboard
devmake graph projects/MyApp.yaml
devmake plan projects/MyApp.yaml
devmake apply projects/MyApp.yaml
```

The architecture should support this flow cleanly and explicitly.

---

## Resolution Pipeline

The current generation path follows a layered resolution process.

### Input layers

1. **Raw document**
   - the project YAML file the user passes in

2. **Resolved document**
   - the normalized project after preset resolution

3. **Render context**
   - the structured values passed into planning and templates

### Practical flow

```text
project file
  ↓
load YAML
  ↓
resolve project through stack/app presets
  ↓
build render context
  ↓
discover plugins
  ↓
build dependency graph
  ↓
create execution plan
  ↓
apply plan into output/
```

This means project generation is no longer just “read plugins from one YAML file and write templates.” It now includes a real resolution step.

---

## Preset Resolution

ForgeStack now supports a model where a project file points to a stack preset and an app preset.

### Example project object

```yaml
kind: project
name: MyApp
uses:
  stack: web-stack
  app: finance-dashboard
overrides: {}
```

The resolver loads the referenced presets and merges them into an effective project shape before planning begins.

That effective project shape is then used to:

- determine plugin set
- determine features
- determine values
- build render context
- drive output generation

This is one of the most important architectural shifts in the platform.

---

## Render Context

Once the raw project and resolved project are known, ForgeStack builds a render context for plugins and templates.

That render context includes things such as:

- raw project document
- effective resolved document
- project name
- stack object
- app object
- values
- plugin list
- feature list
- feature booleans

This allows generation to stay declarative while still giving templates access to the information they need.

### Architectural consequence

This means the current generation system is no longer just plugin-name based. It is project-model aware.

---

## Plugin Planning Model

ForgeStack still follows a **small core, plugin-driven behavior** model.

The core is responsible for:

- configuration loading
- preset resolution
- plugin discovery
- dependency resolution
- graph building
- plan construction
- execution

Plugins are responsible for declaring what should be generated.

### Current plugin behavior

Plugins typically contribute actions like:

- create file
- choose template
- declare dependency requirements

The current architecture still follows the rule:

**Core coordinates. Plugins declare. Executor applies.**

---

## Dependency Graph and Plan

The dependency graph remains a first-class primitive.

### Why it matters

The graph determines:

- plugin ordering
- execution waves
- dependency-aware planning
- explainability for graph and plan commands

### Current planning path

```text
requested or resolved plugins
  ↓
dependency expansion
  ↓
graph build
  ↓
topological ordering
  ↓
plugin planning hooks
  ↓
plan actions
```

This is still one of the core strengths of ForgeStack.

---

## Template System

ForgeStack uses internal templates under:

```text
forgestack/templates/
```

These are implementation details, not user-facing presets.

Current template behavior includes:

- canonical template IDs
- template alias resolution where needed
- file rendering through context-driven templates
- feature-aware rendering

The schema and CLI should stay above this implementation layer.

In other words:

- users interact with stack/app/project/presets
- the engine maps those to plugins and templates internally

---

## Current Generated Output Direction

ForgeStack has now moved into generating a more complete runnable starter app.

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

This is much closer to a real generated application skeleton than the earlier simple-file demo stage.

---

## Current Runtime Milestone

The project has already crossed an important threshold:

### From
- declarative preset-driven scaffolding

### To
- preset-driven generation of a runnable full-stack starter app

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
- backend queues a background task
- frontend displays the results of that flow

This is the key current architectural milestone.

---

## Current Milestone Direction

The project has been moving through an application-skeleton phase in which generation is no longer judged only by “did files get written,” but by “did a coherent runnable starter app get produced.”

That means the current architecture should support:

- generation correctness
- configuration correctness
- runtime wiring correctness
- clearer full-stack output
- stronger generated app behavior

This is a major shift from early scaffold thinking.

---

## What This Architecture Is Not

The current architecture is **not**:

- a return to the old examples-only model
- a widgets-first model
- a stack-only configuration model
- a filesystem-path-first schema
- a finished multi-tool platform runtime
- a full hub platform yet

It is the current stable bridge between the original plugin engine and the more mature preset/project/output model.

---

## Near-Term Architectural Priorities

The main near-term architectural priorities are:

1. keep the stack/app/project/output model stable
2. keep `presets/`, `projects/`, and `output/` cleanly separated
3. keep the CLI aligned with explicit project creation
4. strengthen the generated application skeleton path
5. harden tests around generated output and runtime behavior
6. reduce ambiguity between user-facing presets and internal templates

These are the priorities that protect the architecture from drifting backward.

---

## Relationship to Future Strategy

ForgeStack may later expand into:

- stronger data-science tooling
- technician tooling
- partial frontends
- local-processing systems
- SQLite-backed lightweight systems
- hub-oriented application patterns
- broader tool-family separation

But those future lanes should be built on top of this current architecture, not used to redefine it prematurely.

That is why the object model and project-resolution path are so important now.

---

## Design Rule

The current architecture should remain aligned with the canonical object model and the current CLI path.

That means:

- stack remains reusable technical composition
- app remains reusable product/archetype composition
- project remains the concrete instance
- output remains the generated result

ForgeStack should continue to grow from this structure rather than slipping back into mixed, hard-to-scale configuration patterns.
