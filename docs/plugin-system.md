<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** [Prev: Stack Format](stack-format.md)  
> **Related:** [Core Engine](core-engine.md)

# Plugin System

## Purpose

ForgeStack is a plugin-driven platform.

Plugins are the main extension mechanism through which ForgeStack generates different kinds of systems while keeping the core small.

The plugin system is one of the most important structural parts of the platform because it allows ForgeStack to expand into new lanes without turning the core into a hard-coded collection of framework-specific behavior.

---

## What Plugins Do

Plugins describe generation behavior.

A plugin may:

- declare dependencies
- contribute generation actions
- choose or reference templates
- contribute service-oriented generation behavior
- participate in planning

Plugins are how ForgeStack expands into:

- frontend support
- backend support
- storage support
- worker support
- workflow support
- future data or device lanes

---

## What Plugins Should Not Do

Plugins should not bypass the core architecture.

That means they should not:

- directly replace planning
- introduce uncontrolled side effects during discovery or planning
- embed unrelated global business logic
- treat the core object model as optional
- mutate the filesystem outside the planned apply path without a very good reason

ForgeStack plugins should participate in the architecture, not work around it.

---

## Current Role in ForgeStack

The current active path uses plugins to contribute the generated full-stack starter system.

Examples include plugins for:

- python
- fastapi
- react
- postgres
- redis
- celery

These plugins contribute to the current generated application path while relying on the same shared mechanisms:

- project resolution
- render context
- dependency graph
- planner
- executor

This is what makes the plugin system practical rather than theoretical.

---

## Plugin Responsibilities

A plugin typically handles things like:

### 1. Dependency declaration
Example:
- `fastapi` depends on `python`
- `celery` depends on `redis`

### 2. Plan contribution
A plugin adds actions such as:
- create file
- render template
- add supporting generated files

### 3. Template use
A plugin may reference internal templates under `forgestack/templates/`.

### 4. Feature-aware generation
A plugin may respond to render context features and values.

These are all appropriate plugin responsibilities.

---

## Relationship to the Object Model

Plugins operate **within** the current canonical object model.

That means plugins are not the top-level model themselves.

The top-level user-facing model is:

- stack
- app
- project
- output

Plugins are part of how those higher-level objects get turned into generated results.

This distinction matters because ForgeStack should remain:

- preset-driven at the user level
- plugin-driven at the implementation level

That separation is healthy.

---

## Relationship to the Planner

Plugins should declare intent and let the planner collect that intent into a coherent plan.

### Good plugin behavior
- declare dependencies
- add create/update/patch actions
- select templates
- respond to resolved context

### Bad plugin behavior
- directly perform uncontrolled side effects
- bypass the planner
- duplicate core resolution logic
- treat plan/apply separation as optional

Plugins should help maintain the planner/executor split, not weaken it.

---

## Why the Plugin System Matters

The plugin system is what allows ForgeStack to remain broad in possibility while staying small in the core.

Without plugins, the core would need to understand every future lane directly.

With plugins, ForgeStack can expand into:

- richer application generation
- data-science tooling
- technician workflows
- partial frontends
- local-processing systems
- future hardware or hub-oriented lanes

This is why the plugin system is central to long-term scalability.

---

## Current Scope vs Future Scope

### Current practical plugin scope
Right now, the most important plugins are the ones that support the current connected starter-app path.

That is the active trust-building path.

### Future plugin scope
Later, plugins may broaden into lanes such as:

- jupyterlab
- notebook
- voila
- kedro
- sqlite
- arduino
- broader operational or workflow plugins

Those future possibilities are important, but they should not distract from making the current plugin path solid first.

---

## Design Rule

The plugin system should preserve one central principle:

**plugins extend ForgeStack by declaring generation behavior inside the shared object model, graph, planner, and executor architecture.**

That means the plugin system should help the platform grow without turning the core into a mess.

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** [Prev: Stack Format](stack-format.md)  
**Related:** [Core Engine](core-engine.md)
