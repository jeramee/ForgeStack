<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** Extended Maintainer Notes  
> **Related:** [Architecture](architecture.md)

# ForgeStack Architecture Spec

## Purpose

This document is an **extended maintainer-oriented architecture note** for ForgeStack.

It exists to go deeper than the main [Architecture](architecture.md) document without competing with it.

Use this file when you want:

* a more detailed internal architecture view
* maintainer-oriented structural guidance
* deeper discussion of engine boundaries
* a longer-range internal design reference

Use [Architecture](architecture.md) first for the current canonical architecture.

ForgeStack is a modular platform for generating applications and workflow systems from composable presets and plugins.

Its current active CLI is **`devmake`**.

---

## Relationship to the Main Architecture Doc

This document should be read as:

* **secondary to** `architecture.md`
* **deeper than** `architecture.md`
* **maintainer-facing**
* **less user-facing**
* **more structural and explanatory**

It should not redefine the main current architecture.

The canonical current architecture remains centered on:

* stack
* app
* project
* output
* presets
* projects
* output
* internal templates
* `devmake` as the active CLI

---

## Architectural Thesis

ForgeStack should remain a **small core with plugin-driven behavior**.

The core should coordinate:

* loading
* resolution
* graphing
* planning
* execution
* validation

Plugins should declare:

* dependencies
* generated files
* template usage
* service-oriented generation behavior

The executor should apply the resulting plan.

This remains the governing architectural rule:

**Core coordinates. Plugins declare. Executor applies.**

---

## Design Goals

ForgeStack should preserve several architectural properties as it grows.

### 1. Small core

The core should stay compact and stable.

### 2. Declarative project model

The platform should operate through a clear object model, not mixed all-in-one config files.

### 3. Plan before apply

Generation should remain previewable before execution.

### 4. Graph first

Dependency relationships should remain explicit and inspectable.

### 5. Plugin-led expansion

Most domain-specific behavior should live outside the core.

### 6. Future-lane compatibility

The architecture should remain general enough to support future workflow, technician, data, and hub-oriented expansion without breaking the current model.

---

## Canonical Object Model

ForgeStack is now organized around four primary objects:

* **stack**
* **app**
* **project**
* **output**

### Meanings

#### Stack

Reusable technical preset.

#### App

Reusable product or archetype preset.

#### Project

Concrete instantiated object that combines stack + app + overrides.

#### Output

Rendered filesystem result.

This is a major improvement over the older mixed stack-only approach.

---

## Current Repository Shape

The current recommended repository shape is:

```text
presets/
  stack/
  app/

projects/

output/

forgestack/
  templates/
```

### Notes

* `presets/stack/` contains reusable technical presets
* `presets/app/` contains reusable product presets
* `projects/` contains concrete project objects
* `output/` contains rendered results
* `forgestack/templates/` contains internal render templates

The architecture should keep these layers conceptually distinct.

---

## Layered Architecture

A useful way to think about ForgeStack internally is as several layers.

### Layer 1 - User-facing model

* stack presets
* app presets
* project objects
* output folders

### Layer 2 - Resolution layer

* project loading
* preset resolution
* normalized effective document construction
* render-context assembly

### Layer 3 - Planning layer

* plugin discovery
* dependency resolution
* graph building
* action planning

### Layer 4 - Execution layer

* apply executor
* file creation
* file updates
* output writing

### Layer 5 - Future support layer

* validation
* state
* diff/upgrade potential
* machine-readable plan outputs
* broader tool-family evolution

This layered view helps keep implementation responsibilities clear.

---

## Current High-Level Flow

The current architecture follows this path:

```text
project file
  ->
load YAML
  ->
resolve stack/app presets
  ->
build effective project
  ->
build render context
  ->
discover plugins
  ->
build dependency graph
  ->
create plan
  ->
execute plan
  ->
write output/
```

This is the right conceptual backbone for the current ForgeStack implementation.

---

## Resolution Layer

The resolution layer is one of the biggest architectural shifts in the platform.

### Why it matters

Earlier models treated generation as mostly:

```text
config file -> plugin list -> template writes
```

The current architecture is more mature:

```text
project object -> preset resolution -> effective document -> render context -> planning
```

That means generation now depends on more than just plugin names.

It depends on:

* resolved technical composition
* resolved app/archetype composition
* project name
* merged values and overrides
* resolved features
* explicit object identity

This gives the system more structure and better long-term scalability.

---

## Render Context Model

A critical internal concept is the **render context**.

This is the structured data passed into planning and templates after resolution.

Typical render context inputs include:

* raw project document
* effective resolved document
* project name
* stack data
* app data
* values
* features
* plugin names
* feature booleans

### Architectural benefit

This means templates and generation logic can remain declarative while still seeing rich resolved information.

### Architectural risk to avoid

Do not let templates become the place where core semantic logic lives.

Templates should render from context, not become the primary source of business rules.

---

## Plugin Architecture

ForgeStack remains plugin-driven.

Plugins should focus on declaring generation intent.

Typical plugin responsibilities include:

* declaring dependencies
* adding file-generation actions
* selecting templates
* contributing service-level generation steps

Plugins should not become mini-executors that bypass the planner.

That would weaken the core architecture.

### Good plugin behavior

* describes actions
* uses context
* participates in the plan

### Bad plugin behavior

* performs uncontrolled side effects directly
* embeds too much global logic
* duplicates resolution logic that belongs in the core

---

## Dependency Graph

The dependency graph remains a core primitive.

### Why it still matters

The graph gives ForgeStack:

* deterministic ordering
* inspectability
* diagnostic clarity
* execution waves
* a foundation for future machine-readable tooling

### Internal role

The graph should remain a real internal model, not just a visualization side feature.

This matters because the graph is one of the things that distinguishes ForgeStack from a simple scaffold command.

---

## Planning Layer

The planning layer converts resolved project state and plugin declarations into a concrete plan.

### Main responsibilities

* topological ordering
* plugin planning execution
* plan action collection
* plan validation
* deterministic output preparation

### Desirable properties

The planner should remain:

* deterministic
* inspectable
* easy to test
* easy to reason about
* separated from execution

This split is important enough that it should remain one of the strongest design locks in the codebase.

---

## Executor Layer

The executor applies the plan to the filesystem.

It should remain intentionally less "smart" than the planner.

### Executor responsibilities

* create files
* write files
* update files
* patch files
* materialize output tree

### What the executor should not do

* reinterpret semantic project meaning
* resolve stack/app relationships
* inject business logic that belongs earlier
* become a second planner

Keeping the executor simpler helps keep generation behavior understandable.

---

## Template Architecture

Templates are internal implementation assets.

They live under:

```text
forgestack/templates/
```

These templates should remain below the user-facing schema boundary.

### Important rule

The schema should remain about:

* stack
* app
* project
* preset
* plugin
* overrides
* output

It should not drift into exposing low-level filesystem template rules as user-facing concepts.

### Practical consequence

Users should think in terms of:

* presets
* projects
* output

Maintainers can think in terms of:

* plugins
* plans
* templates
* render contexts

This is a healthy separation.

---

## Current Runtime Direction

The architecture has already moved into a phase where runtime behavior matters, not just file generation.

ForgeStack is no longer judged only by:

* "did the files get created"

It is also judged by:

* "did the generated app actually wire together correctly"

This has already shown up in the current generated starter path, which now includes:

* React frontend
* FastAPI backend
* Redis
* Postgres
* Celery
* Docker build flow
* configuration endpoint
* task queue flow

This is an important maturity shift.

---

## Current Architectural Milestone

The current project has crossed from:

* preset-driven scaffolding

to:

* preset-driven generation of a runnable connected full-stack starter application

That change means the architecture now has to support:

* richer output contracts
* runtime wiring correctness
* app-level behavior generation
* more meaningful template integration
* stronger generated test expectations

This is one of the reasons the current architecture docs needed to be updated.

---

## Future-Lane Compatibility

The architecture should stay general enough to support future lanes such as:

* data-science tooling
* technician tooling
* workflow systems
* SQLite-backed local processing
* partial frontends
* mobile-responsive operational views
* hub-oriented application patterns
* future ForgeStack tool-family separation

But those lanes should be added through:

* presets
* plugins
* additional tools
* roadmap phases

They should not require redefining the core object model.

---

## Tool-Family Compatibility

ForgeStack is the platform.

`devmake` is the current active tool.

This document may acknowledge that broader tool-family growth is possible, but it should not treat future tools as part of the current implemented architecture.

The platform should evolve outward from the current model, not away from it.

---

## What This Spec Should Not Do

This architecture spec should not:

* compete with `architecture.md`
* reintroduce the old stack-only model
* imply that the active CLI is already `forgestack`
* center the docs on `examples/`
* overstate future categories as if they are already implemented
* bury the current object model under abstract framework language

Its role is to deepen the maintainer view, not to confuse the public-facing architecture story.

---

## Maintainer Guidance

When making core design changes, ask:

1. Does this preserve the stack/app/project/output model?
2. Does this belong in the core or should it be a plugin?
3. Does this strengthen or weaken the plan-before-apply split?
4. Does this make the graph more or less meaningful?
5. Does this add clarity to the resolution pipeline?
6. Does this keep templates below the schema boundary?
7. Does this help the current generated app path without destabilizing the model?

These are better questions than "can we just make this work quickly?"

---

## Design Rule

ForgeStack should continue evolving from a clean architectural center:

* small core
* explicit object model
* layered resolution
* graph-first planning
* executor-based apply
* plugin-led expansion

That is the structure that can support both the current product and the broader platform it may become later.

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** Extended Maintainer Notes  
**Related:** [Architecture](architecture.md)
