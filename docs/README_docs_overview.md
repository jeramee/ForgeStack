# ForgeStack Documentation Overview

This documentation set reflects the current ForgeStack direction.

ForgeStack is a modular platform for generating applications and workflow systems from composable presets and plugins.

Its current active CLI is **`devmake`**.

The project is now centered on a clearer object model than the older stack-only approach:

- **stack** = technical preset
- **app** = product or archetype preset
- **project** = concrete instance
- **output** = rendered filesystem result

This documentation is organized to match that direction.

---

## How to Read These Docs

If you are new to ForgeStack, start with the documents that explain the current model and current workflow first.

If you are working on the engine itself, the internal architecture and engine docs are the next layer.

If you are thinking about future positioning, tool-family growth, or roadmap planning, use the strategy documents last.

---

## Start Here

### 1. Introduction
- [Introduction](introduction.md)

High-level explanation of what ForgeStack is, what problem it solves, and how it is currently meant to be used.

### 2. Current Architecture
- [Current Architecture](current-architecture.md)

A practical description of the current implemented direction:
- presets
- projects
- output
- plugin planning
- generated full-stack starter apps
- current runtime milestones

### 3. CLI
- [CLI](cli.md)

Current command surface for `devmake`, including:
- preset discovery
- project creation
- graph
- plan
- apply

### 4. Object Model
- [Object Model](object-model.md)
- [Presets and Projects](presets-and-projects.md)

The canonical model for:
- stack presets
- app presets
- project objects
- output artifacts
- overrides

---

## Core Engine and Internals

These documents describe how ForgeStack works internally.

- [Core Engine](core-engine.md)
- [Graph Engine](graph-engine.md)
- [Planner](planner.md)
- [Executor](executor.md)
- [Validation and State](validation-and-state.md)
- [Machine Readable Output](machine-readable-output.md)
- [Plugin System](plugin-system.md)

Use these when working on:
- plugin planning
- dependency resolution
- template rendering
- apply execution
- validation rules
- future extensibility

---

## Strategy and Product Direction

These documents explain where ForgeStack is going, without changing the locked core model.

- [Product Strategy](product-strategy.md)
- [Data Science Strategy](data-science-strategy.md)
- [Hardware Strategy](hardware-strategy.md)
- [Roadmap](roadmap.md)
- [Platform Tools](platform-tools.md)

These are useful for understanding:
- near-term priorities
- 1.0 / 1.5 / 2.0 direction
- stronger data-science / technician wedge
- future hub-oriented expansion
- planned ForgeStack tool families beyond `devmake`

---

## Extended Design Notes

- [ForgeStack Architecture Spec](forgestack_architecture_spec.md)

This contains deeper internal architecture discussion and broader structural thinking for maintainers.

---

## Recommended Reading Order

### For new users
1. [Introduction](introduction.md)
2. [CLI](cli.md)
3. [Object Model](object-model.md)
4. [Presets and Projects](presets-and-projects.md)
5. [Current Architecture](current-architecture.md)

### For contributors
1. [Introduction](introduction.md)
2. [Current Architecture](current-architecture.md)
3. [Plugin System](plugin-system.md)
4. [Planner](planner.md)
5. [Executor](executor.md)
6. [Validation and State](validation-and-state.md)

### For strategy and roadmap planning
1. [Product Strategy](product-strategy.md)
2. [Roadmap](roadmap.md)
3. [Data Science Strategy](data-science-strategy.md)
4. [Hardware Strategy](hardware-strategy.md)
5. [Platform Tools](platform-tools.md)

---

## Current Documentation Direction

ForgeStack documentation should reflect the current canonical project model, not the older mixed stack-only format.

That means documentation should consistently reflect:

- `devmake` as the current active CLI
- `presets/stack/`
- `presets/app/`
- `projects/`
- `output/`
- the stack/app/project/output object model
- the current connected generated full-stack app path

As the platform expands, future docs may describe additional tools, workflows, and product lanes, but those should build on top of the same core model rather than replace it.
