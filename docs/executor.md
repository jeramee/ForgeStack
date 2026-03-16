<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** [Prev: Planner](planner.md) | [Next: Validation and State](validation-and-state.md)  
> **Related:** [Current Architecture](current-architecture.md)

# Executor

## Purpose

The executor applies the generation plan to the filesystem.

It is the component responsible for materializing the output tree after the planner has already decided what should happen.

The executor is intentionally simpler than the planner.

Its role is not to reinterpret the project model. Its role is to apply the plan.

---

## What the Executor Owns

The executor owns:

- plan action application
- file creation
- file writing
- file updating
- patch application
- output tree materialization

It is the layer that turns plan actions into actual generated files and folders.

---

## What the Executor Does Not Own

The executor should not:

- resolve presets
- determine plugin dependencies
- infer project meaning
- decide feature or workflow semantics
- become a second planner
- introduce hidden business logic during apply

If the executor becomes too smart, the architecture becomes harder to reason about.

---

## Current Role in ForgeStack

The executor runs after:

- project resolution
- render-context assembly
- dependency resolution
- graph construction
- planning
- plan validation

At a high level:

```text
resolved project
  ->
planner
  ->
plan
  ->
executor
  ->
output/
```

This keeps generation split into:

- deciding what should happen
- applying what should happen

That separation is one of the most important architectural rules in ForgeStack.

---

## Why the Executor Should Stay Simple

ForgeStack is growing toward richer generated systems.

That can create a temptation to put more "intelligence" into the executor.

That would be a mistake.

The executor should stay simpler because:

- it improves predictability
- it improves testability
- it keeps planning and execution separate
- it reduces hidden behavior
- it makes plan inspection more trustworthy

If a user inspects a plan, apply should behave consistently with that plan.

---

## Typical Executor Actions

A ForgeStack executor may apply actions such as:

- create directory
- create file
- write rendered content
- update file
- patch file
- materialize generated project structure

These are output actions, not semantic decisions.

---

## Relationship to the Object Model

The executor operates **after** the object model has already been resolved.

That means it should not need to think in deep semantic terms about:

- which stack was selected
- which app was selected
- what the project means conceptually

Those questions are answered earlier in the pipeline.

By the time execution happens, the executor should mostly be concerned with:

- action type
- action path
- action payload
- output root

---

## Current Importance

As ForgeStack moves into generating richer starter applications, executor quality matters more.

That is because apply is no longer judged only by whether files exist afterward.

It is now judged by whether the generated output is coherent enough to run and support the intended starter behavior.

So the executor must be:

- reliable
- deterministic
- aligned with planner output
- careful with file operations
- easy to test

---

## Current Near-Term Priorities

The executor should continue improving in these ways:

1. reliable plan application
2. clean output-root handling
3. consistent file writes
4. support for current create/update/patch needs
5. tighter alignment with generated full-stack output expectations

The executor should not be the place where future platform ambitions are jammed in prematurely.

---

## Design Rule

The executor should remain the apply layer of ForgeStack:

- the planner decides
- the executor materializes
- output reflects the plan
- execution does not redefine meaning

That is what keeps apply trustworthy.

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** [Prev: Planner](planner.md) | [Next: Validation and State](validation-and-state.md)  
**Related:** [Current Architecture](current-architecture.md)