<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** [Prev: Core Engine](core-engine.md) | [Next: Planner](planner.md)  
> **Related:** [Plugin System](plugin-system.md)

# Graph Engine

## Purpose

The graph engine maintains ForgeStack’s dependency graph.

This graph represents the dependency relationships between plugins involved in generation.

The graph is not just a visualization tool. It is a real internal primitive used to support:

- ordering
- dependency expansion
- diagnostics
- explainability
- planning

---

## Why the Graph Matters

ForgeStack is not a flat file generator.

A generated system may involve multiple plugins with dependency relationships, such as:

- frontend frameworks
- backend frameworks
- databases
- queues
- worker systems
- supporting services

Those relationships need to be represented explicitly.

The graph is what allows ForgeStack to remain:

- dependency-aware
- deterministic
- inspectable
- explainable through CLI commands like `graph` and `plan`

---

## Current Role in ForgeStack

The graph is built after:

- project loading
- preset resolution
- plugin discovery
- dependency resolution

And before:

- planning
- plan display
- apply execution

At a high level:

```text
resolved plugin set
  ↓
dependency graph
  ↓
ordered planning
  ↓
plan
```

This is why the graph remains one of the core internal models.

---

## What the Graph Owns

The graph owns the explicit relationship model between plugins.

That includes:

- nodes
- edges
- dependency direction
- graph-based ordering support

The graph gives structure to the generation pipeline.

---

## What the Graph Does Not Own

The graph should not:

- replace preset resolution
- define product meaning
- own output rendering
- own filesystem behavior
- become a general-purpose unrelated runtime graph

Its job is focused: represent generation dependencies clearly.

---

## Relationship to the Current Object Model

ForgeStack now resolves projects through:

- stack presets
- app presets
- project objects

The graph does **not** replace those higher-level objects.

Instead, the object model eventually resolves into a plugin set, and the graph represents the dependency structure of that resolved set.

So:

- object model gives high-level semantic structure
- graph gives dependency structure for planning

This distinction is important.

---

## Graph Benefits

### 1. Ordering
The graph provides valid plugin ordering for planning.

### 2. Explainability
Users can inspect dependency structure with `devmake graph`.

### 3. Diagnostics
Missing dependencies or bad relationships are easier to detect.

### 4. Future tooling
The graph provides a foundation for:
- better machine-readable outputs
- richer diagnostics
- future optimization or visualization work

These benefits are why the graph should remain first-class.

---

## CLI Relevance

The graph is already part of the user-facing workflow:

```powershell
devmake graph projects/MyApp.yaml
```

That means it is not just an internal abstraction. It is part of how ForgeStack explains itself.

A meaningful graph command is one of the reasons ForgeStack feels like a platform rather than only a scaffold shortcut.

---

## Current Design Rule

The dependency graph should remain:

- explicit
- inspectable
- tied to actual planning needs
- central to ordering and diagnostics

It should not be reduced to a decorative feature or hidden implementation detail.

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** [Prev: Core Engine](core-engine.md) | [Next: Planner](planner.md)  
**Related:** [Plugin System](plugin-system.md)
