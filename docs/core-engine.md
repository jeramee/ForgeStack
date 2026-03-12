# Core Engine

## Purpose

The ForgeStack core engine coordinates the generation process.

It is responsible for the parts of the system that should remain small, stable, and shared across all current and future generation lanes.

ForgeStack is a modular platform for generating applications and workflow systems from composable presets and plugins.

Its current active CLI is **`devmake`**.

---

## What the Core Owns

The core owns the platform-level mechanics that every generated system depends on.

That includes:

- loading project input
- resolving stack and app presets
- building the effective project document
- assembling render context
- discovering plugins
- resolving dependencies
- building the dependency graph
- creating the execution plan
- executing the plan
- validating generation behavior

These are the shared coordination responsibilities of ForgeStack.

---

## What the Core Does Not Own

The core should **not** directly own domain-specific generation behavior.

That means it should not become the place where special handling for every framework, service, workflow type, or future product lane gets hard-coded.

Those concerns belong in:

- plugins
- presets
- templates
- future tool-family layers where appropriate

The core should also not become the main place where business-specific rules or product-specific output logic are embedded.

---

## Current Role in ForgeStack

The current core engine sits between the user-facing object model and the generated filesystem output.

At a high level, ForgeStack now works like this:

```text
project file
  ↓
preset resolution
  ↓
render context
  ↓
plugin discovery
  ↓
dependency graph
  ↓
execution plan
  ↓
apply executor
  ↓
output/
```

This makes the core the part of the platform that translates a project definition into a coordinated generation process.

---

## Relationship to the Object Model

The core is now built around the canonical object model:

- **stack**
- **app**
- **project**
- **output**

The core should preserve that model and avoid drifting back into older mixed definitions.

### Stack
Reusable technical preset.

### App
Reusable product or archetype preset.

### Project
Concrete instance that selects stack + app + overrides.

### Output
Rendered filesystem result.

The core’s job is not to redefine these objects, but to coordinate the path from project input to generated output.

---

## Current Responsibilities in More Detail

### 1. Project loading
The core loads the raw YAML project document.

### 2. Preset resolution
The core resolves referenced stack and app presets into an effective project shape.

### 3. Render-context assembly
The core builds the structured context needed by planning and templates.

### 4. Plugin discovery
The core discovers available plugins from the registry.

### 5. Dependency resolution
The core determines which plugins are needed and in what order.

### 6. Graph construction
The core builds the explicit dependency graph.

### 7. Planning
The core coordinates plugin planning hooks and collects plan actions.

### 8. Execution
The core applies the plan into the output tree.

These responsibilities define the core engine boundary.

---

## Current Design Rule

The main design rule remains:

**Core coordinates. Plugins declare. Executor applies.**

This means:

- the core orchestrates
- plugins describe generation behavior
- the executor materializes output

This rule is one of the most important protections against core bloat.

---

## Why the Core Must Stay Small

ForgeStack is expected to expand over time into:

- stronger data-science tooling
- technician tooling
- workflow tooling
- partial frontends
- local-processing systems
- hub-oriented application patterns
- future tool-family layers

That only works if the core remains general and stable.

If every new lane gets hard-coded into the core, the platform becomes:

- harder to reason about
- harder to test
- harder to extend
- harder to trust

A small core is not just a preference. It is a scaling requirement.

---

## Current Near-Term Priorities for the Core

The core should continue to strengthen these areas first:

1. stable stack/app/project/output handling
2. clean preset resolution
3. reliable render-context assembly
4. deterministic graph and planning behavior
5. robust apply execution
6. stronger validation and testability

These are more important right now than adding many new special-case behaviors.

---

## Design Rule

The core engine should remain the stable coordination layer of ForgeStack.

It should preserve:

- the canonical object model
- the plan-before-apply split
- the graph-first mindset
- plugin-driven expansion
- clear separation between user-facing concepts and internal generation mechanics
