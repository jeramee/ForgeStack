<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** [Prev: Executor](executor.md) | [Next: Machine-Readable Output](machine-readable-output.md)  
> **Related:** [Roadmap](roadmap.md)

# Validation and State

## Purpose

Validation and state handling support trust, reproducibility, and future maintainability in ForgeStack.

Validation ensures the system is working with a coherent project definition and coherent generation plan.

State provides a possible foundation for future features such as:

- diff
- upgrade
- drift detection
- ownership tracking of generated files

Validation matters now. State becomes more important as the platform matures.

---

## Validation Layers

ForgeStack should validate at multiple layers.

### 1. Project and preset validation
Validate that:

- the project file exists
- the project shape is valid
- referenced stack presets exist
- referenced app presets exist
- preset structure is valid

### 2. Plugin and registry validation
Validate that:

- plugins exist
- plugin metadata is complete enough to use
- dependencies can be resolved

### 3. Graph validation
Validate that:

- there are no missing dependencies
- there are no invalid cycles
- the dependency model is coherent

### 4. Plan validation
Validate that:

- actions are structurally valid
- paths are acceptable
- conflicting actions are caught
- unsupported action shapes are rejected

This layered approach makes the platform easier to trust.

---

## Why Validation Matters More Now

Earlier scaffold tools can often get away with weak validation.

ForgeStack increasingly cannot.

That is because it is now generating richer starter systems with:

- frontend/backend coordination
- config contracts
- worker wiring
- service composition
- more complete output trees

As generation becomes more meaningful, bad assumptions become more expensive.

Validation is therefore not just defensive programming. It is part of product quality.

---

## Relationship to the Object Model

Validation should now be aligned with the current canonical model:

- stack
- app
- project
- output

That means validation should not think only in terms of:
- a single stack file
- a flat plugin list

Instead, it should validate:

- project references
- preset references
- merged resolved shape
- generation plan coherence

This is one of the ways the newer architecture improves on the older mixed model.

---

## Plan Validation

Plan validation is especially important because ForgeStack follows a plan-before-apply architecture.

If the plan is wrong, apply may still execute mechanically and produce broken output.

That is why plan validation should catch issues such as:

- conflicting actions on the same path
- invalid output paths
- unsupported action kinds
- inconsistent action payloads

The planner and validation layers should work together to prevent obvious bad plans from reaching execution.

---

## State Design

State is more future-facing than validation, but it is still worth describing clearly.

A future ForgeStack state file might track things such as:

- project identity
- plan hash
- generated files
- checksums
- plugin ownership

Example conceptual location:

```text
.forgestack/state.json
```

This would support later lifecycle operations if and when they become important.

---

## Why State Should Stay Modest for Now

State is useful, but it should not become a premature source of complexity.

Right now, ForgeStack benefits more from:

- good object-model clarity
- good plan correctness
- strong output generation
- strong runtime wiring
- strong validation

So state should remain practical and incremental rather than overbuilt.

---

## Future Uses for State

As ForgeStack matures, state may help support:

- diff between generations
- upgrade behavior
- drift detection
- safer regeneration
- plugin ownership tracking
- machine-readable tooling

These are useful goals, but they should come after the current core path is solid.

---

## Design Rule

Validation should be strong enough to protect the current generation path now.

State should be introduced carefully enough to support future lifecycle features later.

Together, they should make ForgeStack more trustworthy without making the core unnecessarily heavy.

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** [Prev: Executor](executor.md) | [Next: Machine-Readable Output](machine-readable-output.md)  
**Related:** [Roadmap](roadmap.md)