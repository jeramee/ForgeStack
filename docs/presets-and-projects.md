# Presets and Projects

ForgeStack separates reusable preset definitions from concrete project instances.

This is one of the most important design rules in the platform.

The current canonical model is:

- **stack preset**
- **app preset**
- **project object**
- **generated output**

This document explains how those pieces relate to each other and how they are expected to live in the repository.

---

## Why This Separation Exists

Older scaffold tools often mix too many concerns into one file:

- technical composition
- product intent
- naming
- overrides
- generated output assumptions

ForgeStack is moving away from that pattern.

Instead, it keeps reusable definitions separate from concrete instances.

That improves:

- clarity
- reuse
- CLI readability
- future expansion
- long-term maintainability

---

## Presets

A **preset** is a reusable configuration object.

ForgeStack currently uses two main preset families:

- **stack presets**
- **app presets**

These are stored under:

```text
presets/
  stack/
  app/
```

Presets are reusable inputs to project creation. They are not generated artifacts and they are not concrete project instances.

---

## Stack Presets

A **stack preset** defines technical composition.

It describes the reusable technical shape of a system.

A stack preset may include:

- plugin list
- service profile
- technical defaults
- capability groupings
- framework and service composition

### Example

```yaml
name: web-stack
kind: stack
summary: Full web application stack with frontend, API, database, cache, and workers.
plugins:
  - react
  - fastapi
  - postgres
  - redis
  - celery
services:
  profile: web
```

### What a stack preset should own

- technical composition
- frameworks
- services
- technical capabilities

### What a stack preset should not own

- final project name
- domain branding
- instance-specific overrides
- generated output paths

---

## App Presets

An **app preset** defines product, archetype, or workflow intent.

It describes what kind of application is being generated at the product level.

An app preset may include:

- feature modules
- workflow shape
- UX shape
- domain intent
- default stack affinity

### Example

```yaml
name: finance-dashboard
kind: app
summary: Dashboard-oriented finance application preset.
stack: web-stack
features:
  - charts
  - auth
  - reporting
  - admin
```

### What an app preset should own

- use case
- features
- workflow-facing intent
- product/archetype identity

### What an app preset should not own

- low-level service wiring
- plugin dependency mechanics
- final project identity
- output layout rules

---

## Projects

A **project** is a concrete instantiated object.

It selects a stack preset and an app preset, gives the instance a real name, and optionally adds overrides.

Projects are stored under:

```text
projects/
```

### Example

```yaml
name: MyApp
kind: project
uses:
  stack: web-stack
  app: finance-dashboard
overrides:
  postgres:
    db: finance_app
  celery:
    workers: 2
```

### What a project should own

- concrete project name
- selected stack preset
- selected app preset
- instance-level overrides
- instance-specific configuration

### What a project should not own

- reusable global preset definitions
- internal rendering rules
- low-level template ownership
- general platform semantics

---

## Output

**Output** is the rendered filesystem result of applying a project.

Generated output is stored under:

```text
output/
```

### Example

```text
output/MyApp/
```

This is the final generated folder tree.

It may contain:

- frontend files
- backend files
- worker files
- Docker files
- environment files
- generated documentation

Output is a result. It is not itself a reusable preset or project definition.

---

## Repository Layout

The current recommended structure is:

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

- `presets/stack/` stores reusable technical presets
- `presets/app/` stores reusable product presets
- `projects/` stores concrete project instances
- `output/` stores generated results
- `forgestack/templates/` stores internal render templates

This structure keeps reusable meaning separate from generated artifacts.

---

## Project Creation Flow

The recommended near-term flow is:

### 1. Discover presets

```powershell
devmake presets list
```

### 2. Create a project

```powershell
devmake create project MyApp --stack web-stack --app finance-dashboard
```

### 3. Inspect graph and plan

```powershell
devmake graph projects/MyApp.yaml
devmake plan projects/MyApp.yaml
```

### 4. Generate output

```powershell
devmake apply projects/MyApp.yaml
```

### 5. Run generated project

```powershell
cd output\MyApp
docker compose up --build
```

---

## Why Project Names Matter

Preset identity and project identity are not the same thing.

For example:

- `web-stack` is a reusable technical preset
- `finance-dashboard` is a reusable app preset
- `MyApp` is the concrete project instance

This distinction is important because a single app preset may be reused many times.

### Example

```powershell
devmake create project CustomerPortal --stack web-stack --app finance-dashboard
devmake create project InternalOps --stack web-stack --app finance-dashboard
```

Same app preset, different project identities.

---

## Why `presets` Is the Preferred Term

ForgeStack uses **presets** as the main organizing term for reusable top-level inputs.

### Preferred
- presets

### Rejected or avoided
- widgets
- examples
- templates as a top-level user-facing label

### Why

- **widgets** sounds like UI components
- **examples** sounds like demo material
- **templates** is overloaded because ForgeStack already has internal file templates

**Presets** best captures reusable stack and app definitions.

---

## Relation to the Object Model

Presets and projects are not separate from the object model. They are the practical filesystem expression of it.

### Object model
- stack
- app
- project
- output

### Filesystem form
- `presets/stack/`
- `presets/app/`
- `projects/`
- `output/`

This alignment between concept and repository structure is intentional.

---

## Design Rule

ForgeStack should keep reusable preset definitions, concrete project instances, and generated output clearly separated.

That means:

- stack presets stay reusable
- app presets stay reusable
- project files stay concrete
- output stays generated

This rule is one of the main protections against drifting back into mixed, hard-to-scale configuration files.