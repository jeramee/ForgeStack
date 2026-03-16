<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** [Prev: Platform Tools](platform-tools.md)  
> **Related:** [Platform Tools](platform-tools.md)

# devdata / devview Boundaries

This document defines the boundary between the future **`devdata`** and **`devview`** tool lanes inside ForgeStack.

It is a **boundary-definition document**, not a repo-split plan and not a new active CLI announcement.

The current implementation rule remains:

- **ForgeStack** is the umbrella platform
- **`devmake`** is the current active CLI
- implementation remains inside the main ForgeStack repo
- future tools may be reserved and documented now
- future tools should only split into standalone repos later if their command surfaces and codebases become mature enough to justify it

---

## Purpose of This Document

The purpose of this milestone is to prevent drift while ForgeStack expands through v1.5.

This document exists to:

- define what belongs to **`devdata`**
- define what belongs to **`devview`**
- clarify what still belongs to **`devmake`**
- map completed v1.5 work into those future lanes
- avoid premature repo fragmentation

It does **not** activate new CLIs.

---

## Current Rule

At this stage, **`devmake` remains the only active public command surface**.

All implementation continues to live in the main ForgeStack repo.

That means:

- no standalone `devdata` CLI yet
- no standalone `devview` CLI yet
- no forced package split yet
- no repo split yet

The lane names are being locked now so future work can be placed consistently.

---

## Boundary Summary

## `devmake`

### Role
`devmake` is the active ForgeStack generation CLI.

### Owns
`devmake` owns the shared generation flow and cross-cutting platform mechanics:

- preset discovery
- preset resolution
- project creation
- dependency graphing
- planning
- apply / generation
- plugin discovery
- output rendering
- stack / app / project / output orchestration

### Does not mean
The existence of future lanes does **not** reduce `devmake` into a temporary throwaway tool.

`devmake` remains the real working CLI and the center of current implementation.

---

## `devdata`

### Role
`devdata` is the future lane for **data work, workflow state, processing, and workbench-oriented operations**.

It should be interpreted broadly, not only as “ML tooling” and not only as notebook tooling.

### Owns
The `devdata` lane should eventually own patterns such as:

- local workflow data/state support
- SQLite-backed operational persistence
- branch or semi-connected workflow state
- staging and ingestion utilities
- processing-side utilities
- data workbench patterns
- Jupyter / JupyterLab workspace patterns
- structured data workflow patterns
- pipeline-oriented workflow systems
- technician-facing data operations
- local-to-central processing support

### Good mental model
If the concern is mainly about **data movement, local state, processing, staging, notebook workspaces, or structured workflow execution**, it probably leans toward `devdata`.

### Explicit non-goals
`devdata` should not become the owner of:

- the main generation lifecycle
- generic preset resolution
- the core planner/executor
- the general project/app/stack/output model
- all UI surfaces by default

Those remain shared platform concerns or belong to `devview` where appropriate.

---

## `devview`

### Role
`devview` is the future lane for **operational surfaces, technician/operator interfaces, dashboards, status views, and published views**.

It should be interpreted broadly, not only as charts and not only as front-end cosmetics.

### Owns
The `devview` lane should eventually own patterns such as:

- technician consoles
- operator panels
- queue/status views
- work-item views
- mobile-responsive operational web surfaces
- monitoring screens
- dashboard-oriented views
- notebook-backed published views
- lightweight operational frontends
- presentation-oriented browser surfaces
- view bridges that publish workflow state or notebook output

### Good mental model
If the concern is mainly about **what a technician, operator, or stakeholder sees and interacts with in a browser or published operational surface**, it probably leans toward `devview`.

### Explicit non-goals
`devview` should not become the owner of:

- core generation flow
- planner/executor internals
- preset resolution
- local processing/state semantics by default
- notebook authoring and processing workflows by default

Those belong to shared ForgeStack core or to `devdata`.

---

## Shared Platform vs Future Tool Lanes

The key design rule is:

- **ForgeStack** owns the shared platform
- **`devmake`** is the current active CLI
- **`devdata`** and **`devview`** are future tool lanes
- lane boundaries should guide architecture now
- lane separation should not force repo separation yet

This means completed v1.5 work can map conceptually into future lanes **without** leaving the main ForgeStack codebase.

---

## Mapping Completed v1.5 Work

The completed v1.5 milestones already point toward future boundaries.

## M1.5-A — SQLite + Local Workflow Foundation
Primary future lane: **`devdata`**

Why:

- local workflow state
- SQLite-backed persistence
- operational data at branch/local scale
- processing-side support
- semi-connected workflow foundations

Secondary relationship: may support `devview` indirectly when UI surfaces read from local workflow state.

---

## M1.5-B — Technician Console / Mobile-Responsive Operational Web Surface
Primary future lane: **`devview`**

Why:

- technician-facing browser surface
- operational web UI
- mobile-responsive workflow presentation
- queue summary, quick actions, work items, configuration views

Secondary relationship: depends on workflow/state patterns that lean toward `devdata`.

---

## M1.5-C — Jupyter / JupyterLab Workspace Lane
Primary future lane: **`devdata`**

Why:

- notebook workspace
- data workbench patterns
- technical workflow environment
- processing/workbench orientation

Secondary relationship: notebook outputs may later be exposed through `devview`.

---

## M1.5-D — Voilà View Bridge
Primary future lane: **`devview`**

Why:

- published view bridge
- notebook-backed presentation surface
- user-facing rendered output
- browser-delivered view pattern

Secondary relationship: depends on notebook/workspace patterns that lean toward `devdata`.

---

## Expected Mapping for Later v1.5 Milestones

## M1.5-E — Boundary Definition
This milestone exists to lock the conceptual split itself.

Primary result:

- define lane boundaries
- freeze language
- prevent architectural drift
- keep implementation in ForgeStack

---

## M1.5-F — Kedro / Structured Workflow Lane
Primary future lane: **`devdata`**

Why:

- structured pipelines
- workflow execution
- transformation orchestration
- data/process semantics

---

## M1.5-G — Arduino / First Device Bridge Patterns
Primary relationship: **shared platform**, with likely future connection to **`devhub`** later.

Why:

- device bridge patterns are broader than pure data or pure view
- likely to inform future hub/device coordination architecture
- may expose both state (`devdata`) and surfaces (`devview`) later, but should not be prematurely forced into either lane

---

## M1.5-H — Hardening and Release Prep
Primary relationship: **shared platform**

Why:

- packaging
- release quality
- test hardening
- build/repo stability
- public CLI trust

This milestone strengthens ForgeStack as a platform and `devmake` as the active CLI.

---

## Decision Rules for Future Work

When placing new work, use these rules:

### Put work closer to `devdata` when it is mainly about:
- local state
- SQLite persistence
- workflow data
- processing
- ingestion
- transformation
- workbench tooling
- notebooks
- pipeline structure
- technician-side data operations
- semi-connected execution

### Put work closer to `devview` when it is mainly about:
- dashboards
- technician console surfaces
- operator panels
- queue/status displays
- monitoring screens
- mobile-responsive operational UI
- published notebook views
- browser-facing workflow presentation

### Keep work in shared ForgeStack / `devmake` when it is mainly about:
- preset resolution
- project creation
- planner behavior
- executor behavior
- plugin discovery
- output generation
- stack/app/project/output model
- cross-cutting orchestration

---

## What This Milestone Does Not Do

This milestone does **not**:

- create a standalone `devdata` CLI
- create a standalone `devview` CLI
- split the repo
- split the package into separate products
- replace `devmake`
- alter the canonical stack / app / project / output object model

---

## Locked Outcome

After this milestone, ForgeStack should be understood as follows:

- **ForgeStack** = umbrella platform
- **`devmake`** = active generator CLI
- **`devdata`** = reserved future lane for data/workflow/workbench/state concerns
- **`devview`** = reserved future lane for operational surfaces/published views/browser-facing presentation concerns

Implementation remains in the main ForgeStack repo until later maturity justifies a stronger split.

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** [Prev: Platform Tools](platform-tools.md)  
**Related:** [Platform Tools](platform-tools.md)
