<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** [Prev: Graph Engine](graph-engine.md) | [Next: Executor](executor.md)  
> **Related:** [Current Architecture](current-architecture.md)

# Planner

## Purpose

The planner converts resolved ForgeStack project state into a concrete execution plan.

It is the bridge between:

* the resolved project model
* plugin declarations
* the final set of generation actions

The planner is one of the most important parts of ForgeStack because it allows the platform to remain:

* declarative
* inspectable
* dependency-aware
* testable
* previewable before execution

---

## What the Planner Owns

The planner owns the process of turning resolved inputs into plan actions.

That includes:

* consuming the resolved plugin set
* respecting dependency order
* invoking plugin planning hooks
* collecting actions
* preserving action order where required
* validating plan shape before execution

The planner is where "what should happen" becomes explicit.

---

## What the Planner Does Not Own

The planner should not:

* execute filesystem side effects directly
* resolve business meaning that belongs in presets
* replace the executor
* become a dumping ground for plugin-specific hacks
* duplicate lower-level template rendering concerns unnecessarily

Its job is to build the plan, not to apply it.

---

## Current Role in ForgeStack

In the current architecture, planning happens after:

```
project
  ->
resolve presets
  ->
build render context
  ->
build dependency graph
  ->
create plan
  ->
plan actions
  ->
executor applies plan
```

In the current implementation, this planner role is carried by `forgestack/core/planner.py`, which collects plugin-driven file actions for the active public apply path.


## Relationship to the Object Model

The planner now works from the resolved project model, not from a raw stack-only plugin list.

That means planning is informed by:

* stack preset meaning
* app preset meaning
* project overrides
* resolved features
* resolved values
* plugin dependency structure

This is one of the important differences between the current ForgeStack direction and the older mixed config model.

---

## Current Planning Flow

A useful mental model for the planner is:

1. receive resolved plugin set and render context
2. respect dependency ordering from the graph
3. invoke plugin planning hooks
4. collect plan actions
5. validate the resulting plan
6. hand the plan to the executor

This keeps plan creation explicit and predictable.

---

## Why Plan-Before-Apply Matters

ForgeStack follows a **plan-before-apply** rule.

That means the system should be able to show what it intends to generate before writing output.

### Benefits

* safer generation
* easier debugging
* clearer CI usage
* more reliable testing
* future machine-readable plan support

The planner is the component that makes this rule real.

---

## What a Plan Represents

A plan is the explicit list of generation actions ForgeStack intends to perform.

Typical actions may include:

* create file
* update file
* patch file
* create directory
* add generated content

The plan should be:

* deterministic
* inspectable
* explainable
* close to executor-ready

---

## Plugin Interaction

Plugins contribute to planning by declaring generation intent.

They should not bypass the planner with uncontrolled side effects.

### Good pattern

A plugin says:

* create this file
* use this template
* require this dependency

### Bad pattern

A plugin directly mutates the filesystem or embeds execution logic that the executor should own.

The planner is where those declarations are collected into a coherent output plan.

---

## Dependency Awareness

The planner depends on the dependency graph to determine valid execution order.

This matters because generation is not flat.

A generated system may involve:

* frontend
* backend
* database configuration
* queue configuration
* worker wiring
* shared config generation

Those pieces may need to appear in a valid dependency-aware order.

The planner is where that order becomes operational.

---

## Current Near-Term Importance

As ForgeStack moves toward richer generated starter applications, the planner becomes more important, not less.

That is because generation is no longer only about "writing a few files."

It is now about producing a coherent generated application skeleton with:

* runtime wiring
* config contracts
* task flow behavior
* feature-aware rendering
* full-stack alignment

The planner is the step that makes this all traceable and previewable.

---

## Design Rule

The planner should remain the explicit contract-builder of ForgeStack.

It should take resolved project meaning plus plugin declarations and turn them into a deterministic plan that the executor can apply cleanly.

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** [Prev: Graph Engine](graph-engine.md) | [Next: Executor](executor.md)  
**Related:** [Current Architecture](current-architecture.md)
