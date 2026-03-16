<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** [Prev: Lean Core Principles](lean-core-principles.md) | [Next: Data Science Strategy](data-science-strategy.md)  
> **Related:** [Roadmap](roadmap.md)

# Product Strategy

ForgeStack should be developed in clear phases that match both its current implementation reality and its longer-term platform direction.

ForgeStack is not just a generic scaffold tool. It is becoming a modular platform for generating applications, workflow systems, technician tools, and later more hub-oriented business systems.

Its current active CLI is **`devmake`**.

The strategy should stay disciplined:

- broad enough for general business use
- strongest and most credible first in data-science, technician, and internal workflow tooling
- open to future hub-oriented and device-connected expansion
- not locked into a single narrow vertical identity

---

## Strategic Position

ForgeStack should be positioned as a **preset-driven generation platform** that can grow into a broader workflow and tool-generation system.

### Near-term identity
ForgeStack generates connected starter applications and workflow tools from:

- stack presets
- app presets
- project objects
- dependency-aware plugins
- internal templates

### Strongest near-term wedge
The clearest near-term specialization is:

- data-science tooling
- technician tooling
- internal workflow systems

### Broader market posture
ForgeStack should remain usable in broader business contexts, including:

- internal applications
- dashboards
- workflow panels
- local-processing tools
- operational frontends

### Future direction
Longer term, the same architecture may support:

- partial frontends
- mobile-responsive operational interfaces
- local-to-central processing systems
- hub-oriented application patterns
- broader platform tooling beyond `devmake`

This broader direction is important, but it should be layered on top of the current architecture rather than used to destabilize it.

---

## Strategic Rule

ForgeStack should be **general in architecture** and **specific in its strongest early wedge**.

That means:

- do not over-specialize the core product around one niche
- do not present the product as if every future lane is already active
- do build toward a strong master-of-one identity in the near term

A good expression of that is:

- **jack of many workflows**
- **master first in data-science / technician / workflow tooling**

---

## Current Product Stage

ForgeStack has already moved past a pure concept phase.

It has crossed from:

- plugin-demo scaffolding

into:

- preset-driven generation of a runnable connected starter application

The platform now has enough shape to justify a stronger product strategy with phased releases rather than open-ended exploration.

---

## Phase 1 — Stable Core / Golden Path

### Goal
Ship ForgeStack as a reliable preset-driven generation system with a strong core experience.

### Primary outcomes
- stabilize the object model
- stabilize the current CLI
- make generated output feel real and usable
- prove that a stack preset + app preset + project object can generate a coherent runnable system

### Core scope
- `stack`
- `app`
- `project`
- `output`
- `presets/`
- `projects/`
- `output/`
- `devmake` as active CLI

### Canonical 1.0 generation story
Generate a connected starter application with:

- React frontend
- FastAPI backend
- PostgreSQL
- Redis
- Celery
- Docker build flow

### Key requirements
- plan-before-apply
- dependency-aware plugin planning
- clean preset resolution
- stronger generated full-stack output
- explicit project creation workflow
- documentation that reflects the real current model

### Product meaning
In this phase, ForgeStack is primarily:

**a preset-driven application generator**

---

## Phase 1.5 — Workflow and Technician Expansion

### Goal
Expand beyond the single web-app golden path into stronger workflow and technician-oriented use cases.

### Why this phase matters
This is where ForgeStack becomes more than “app scaffolding” and starts becoming a generator for practical internal tools and operational systems.

### Focus areas
- JupyterLab / Notebook
- Voilà
- Kedro
- SQLite
- technician-oriented presets
- workflow-oriented presets
- partial frontends
- mobile-responsive operational frontends

### Why SQLite matters
SQLite should become a first-class option for:

- local workflow tools
- local processing stages
- temporary staging
- OCR/document metadata staging
- lightweight operational tools
- technician-side or branch-side persistence

This complements PostgreSQL rather than replacing it.

### Product meaning
In this phase, ForgeStack becomes:

**an application, workflow, and technician-tool generator**

---

## Phase 2 — Hub-Oriented Platform Expansion

### Goal
Expand ForgeStack into a broader platform for hub-connected business workflows, multi-surface frontends, and richer operational ecosystems.

### Focus areas
- broader partial frontend strategy
- local/central workflow patterns
- stronger business-device hub positioning
- future tool-family expansion
- broader backend and device integration lanes

### Possible future tool families
- `devdata`
- `devview`
- `devhub`
- `devai`
- `devpkg`

### Product meaning
In this phase, ForgeStack becomes:

**a broader workflow and hub-oriented generation platform**

This is the point where ForgeStack can support not just application generation, but a family of related operational tools and generated system patterns.

---

## Market Positioning

ForgeStack should not be boxed into only one future.

It should remain capable of serving:

- internal business applications
- data-science tooling
- technician workflows
- local-processing tools
- workflow systems
- future operator or hub-facing frontends

That broader positioning is valuable.

At the same time, the product should avoid pretending all of those lanes are equally mature right now.

The documentation and product messaging should reflect:

- what exists now
- what is near-term
- what is future-facing

---

## What ForgeStack Should Not Become

ForgeStack should not drift into:

- an OCR-only product identity
- a dashboard-only identity
- a stack-only configuration model
- a generic everything-platform with no strong wedge
- a core bloated with domain-specific behavior that should live in plugins

Its strength is the combination of:

- clean object model
- lean core
- plugin-driven expansion
- practical workflow generation

---

## Product-Lane Interpretation

### Current lane
Preset-driven application generation.

### Strongest near-term lane
Data-science, technician, and workflow tooling.

### Future high-fit lanes
- partial frontends
- local-processing systems
- workflow and operations tools
- hub-connected business systems
- document or operational workflow applications

These future lanes are examples of where the platform can go. They should not redefine the core platform prematurely.

---

## Strategic Design Principle

ForgeStack should keep one central rule:

**stabilize the core model first, then broaden the platform in deliberate waves.**

That means:

- v1.0 is about credibility and coherence
- v1.5 is about practical expansion
- v2.0 is about platform breadth

That sequence is what gives the product a believable path from useful tool to broader system.

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** [Prev: Lean Core Principles](lean-core-principles.md) | [Next: Data Science Strategy](data-science-strategy.md)  
**Related:** [Roadmap](roadmap.md)