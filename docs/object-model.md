<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** [Next: Presets and Projects](presets-and-projects.md)  
> **Related:** [Architecture](architecture.md)

# Object Model

ForgeStack is built around a small declarative object model.

This model separates reusable technical composition, reusable product intent, concrete project identity, and generated filesystem results.

The canonical objects are:

- **stack**
- **app**
- **project**
- **output**

This is a core design decision for ForgeStack.

---

## Why the Object Model Matters

Older scaffold tools often mix too many concerns into one file:

- technical stack selection
- feature intent
- project identity
- service overrides
- generated output assumptions

ForgeStack is moving away from that mixed approach.

The object model exists so that each layer has a clear job and a clear boundary.

---

## Core Objects

## 1. Stack

A **stack** is a reusable technical preset.

It defines the technical composition of a generated system.

A stack may own:

- frameworks
- services
- plugin selection
- technical profile
- service categories
- capability defaults

A stack should **not** own:

- final project identity
- product naming
- domain branding
- specific workflow intent that belongs to the app layer

### Example responsibilities
- React + FastAPI + Postgres + Redis + Celery
- API-only stack
- ML-oriented technical stack

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

---

## 2. App

An **app** is a reusable product or archetype preset.

It defines product-facing or workflow-facing intent.

An app may own:

- use case
- feature modules
- UX shape
- workflow shape
- domain intent
- default stack affinity

An app should **not** own:

- low-level service wiring
- infrastructure details
- plugin dependency mechanics that belong to the stack layer

### Example responsibilities
- finance dashboard
- data science dashboard
- technician console
- workflow application
- operator panel

### Example
```yaml
name: finance-dashboard
kind: app
summary: Dashboard-oriented finance application preset.
stack: web-stack
features:
  charts: true
  auth: true
  reporting: true
  admin: true
```

---

## 3. Project

A **project** is a concrete instantiated object.

It connects a chosen stack and chosen app into a real named project with optional overrides.

A project may own:

- chosen project name
- selected stack preset
- selected app preset
- concrete overrides
- instance-specific configuration

A project should **not** own:

- global reusable preset definitions
- internal template rules
- generalized system behavior that should stay reusable

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

---

## 4. Output

**Output** is the rendered filesystem result.

It is the generated folder tree produced by applying a project.

Output may own:

- generated files
- generated folders
- generated compose files
- generated frontend/backend/worker code
- generated README or environment files

Output should **not** own:

- semantic preset identity
- reusable stack meaning
- reusable app meaning

### Example
```text
output/MyApp/
```

This folder is the result of generation, not part of the reusable object model itself.

---

## Relationship Between Objects

The relationship is:

```text
stack + app + project overrides
            ->
       resolved project
            ->
          plan
            ->
         output
```

Or more conceptually:

```text
stack = technical composition
app = product/workflow composition
project = concrete instance
output = rendered result
```

---

## Repository Shape

The object model maps directly to the repository structure.

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

- `presets/stack/` stores reusable stack objects
- `presets/app/` stores reusable app objects
- `projects/` stores concrete project instances
- `output/` stores generated results
- `forgestack/templates/` stores internal render templates

This structure helps avoid mixing:
- reusable definitions
- concrete instances
- generated artifacts

---

## Why `presets` Is the Right Term

ForgeStack uses **presets** as the top-level organizing term.

### Why not `widgets`
Too UI-specific. Suggests visual components instead of reusable system definitions.

### Why not `examples`
Too weak. Sounds like demo material instead of reusable project-building objects.

### Why not `templates`
Too overloaded. ForgeStack already uses lower-level internal file templates.

### Why `presets`
Because it naturally describes reusable stack and app configurations.

---

## Separation Rules

### Stack should not become app
A stack should not be overloaded with product identity.

### App should not become stack
An app should not be overloaded with low-level technical wiring.

### Project should not become preset
A project is an instance, not a reusable global definition.

### Output should not become model
Generated files are results, not object definitions.

These rules help keep the platform coherent as it grows.

---

## Why the Older Mixed YAML Model Is Not Enough

Older all-in-one configuration files blur together:

- project identity
- plugin selection
- service configuration
- reusable technical meaning
- reusable product meaning

That works for early bootstrapping, but it does not scale well.

As ForgeStack grows into a platform for:
- generated applications
- workflow systems
- technician tooling
- future hub-oriented systems

the object model needs cleaner boundaries.

---

## Declarative Language Direction

ForgeStack is built around a small declarative language and object model.

Main nouns:

- stack
- app
- project
- preset
- plugin
- output

Main verbs:

- create
- list
- graph
- plan
- apply
- validate

Typical attributes:

- plugins
- services
- features
- capabilities
- workers
- ports
- database settings
- overrides

This makes the CLI and config model easier to understand.

---

## Current Example Flow

### Create a project
```powershell
devmake create project MyApp --stack web-stack --app finance-dashboard
```

### Resulting project object
```yaml
kind: project
name: MyApp
uses:
  stack: web-stack
  app: finance-dashboard
overrides: {}
```

### Then generate output
```powershell
devmake apply projects/MyApp.yaml
```

### Output
```text
output/MyApp/
```

---

## Design Rule

The object model should remain general enough to support future workflow, technician, and hub-oriented application patterns without changing the fundamental separation between:

- stack
- app
- project
- output

That separation is the lock that keeps ForgeStack from drifting back into mixed object definitions.

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** [Next: Presets and Projects](presets-and-projects.md)  
**Related:** [Architecture](architecture.md)