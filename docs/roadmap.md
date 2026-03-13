# Roadmap

This roadmap reflects the current ForgeStack direction.

It is based on the current active CLI (**`devmake`**), the current canonical object model, and the current implementation path around presets, projects, and generated output.

ForgeStack is not being roadmapped as a stack-only CLI anymore. It is being roadmapped as a preset-driven generation platform with phased expansion.

---

## Roadmap Principles

The roadmap should follow a few rules:

- stabilize what is already real before broadening scope
- keep the object model clean
- keep the core small
- add new lanes in deliberate waves
- distinguish clearly between now, near future, and future future

---

## Current State

ForgeStack has moved from early plugin-demo scaffolding into a preset-driven generation platform with multiple implemented vertical slices.

The platform currently centers on:

- stack presets
- app presets
- project objects
- generated output folders
- dependency-aware plugin planning
- internal templates
- `devmake` as the active CLI

Implemented slices now include:

- web-stack connected starter app generation
- SQLite-backed local workflow foundation
- technician console / mobile-responsive operational UI
- Jupyter workspace lane
- Voilà notebook-view bridge
- structured workflow / Kedro scaffold
- Arduino-first device bridge scaffold

The current codebase is now in a hardening and release-prep phase rather than an initial architecture-definition phase.

---

## v1.0 — Stable Core / Connected Starter App

### Goal
Establish the stable core ForgeStack generation path and connected starter-app baseline.

### Main outcomes
- lock the object model
- lock the CLI direction
- harden preset resolution
- harden plan/apply flow
- make generated output consistently runnable
- align docs with the real model

### Core model to lock
- `stack`
- `app`
- `project`
- `output`

### Repository model to lock
```text
presets/
  stack/
  app/

projects/

output/

forgestack/
  templates/
```

### CLI to stabilize
```powershell
devmake plugins
devmake presets list
devmake create project MyApp --stack web-stack --app finance-dashboard
devmake graph projects/MyApp.yaml
devmake plan projects/MyApp.yaml
devmake apply projects/MyApp.yaml
```

### Runtime milestone
A generated full-stack starter app that supports:

- frontend calls backend
- backend exposes real endpoints
- backend returns structured config
- backend queues background work
- frontend displays the result of that flow

### Documentation priorities
- README
- docs overview
- introduction
- CLI
- object model
- presets and projects
- current architecture

### Test priorities
- preset resolution
- render contract correctness
- generated output correctness
- runtime wiring correctness
- task flow correctness

### v1.0 product meaning
ForgeStack is a **preset-driven application generator** with a real connected starter path.

---

## v1.5 — Workflow / Technician / Data Expansion

### Goal
Expand the platform into stronger workflow, technician, and data-oriented use cases.

Much of this phase is now implemented, and the current focus has shifted to hardening and release preparation.

### Main additions
- JupyterLab / Notebook
- Voilà
- Kedro
- SQLite
- workflow-oriented presets
- technician-oriented presets
- partial frontends
- mobile-responsive operational frontends

### Why this phase matters
This is the point where ForgeStack becomes more than a generated web-app starter and starts becoming a platform for practical internal tools.

### SQLite in v1.5
SQLite should be added as a first-class lightweight backend for:

- local workflow systems
- temporary staging
- branch-side tools
- processing-side persistence
- local operational tools

This should complement PostgreSQL, which remains the stronger central multi-user backend.

### v1.5 product meaning
ForgeStack becomes an **application, workflow, and technician-tool generator**.

---

## v2.0 — Hub-Oriented Platform Expansion

### Goal
Expand ForgeStack into a broader platform for hub-connected systems, partial frontends, and richer operational workflows.

### Main additions
- stronger hub-oriented architecture patterns
- broader partial frontend strategy
- local/central deployment patterns
- broader platform tool-family direction
- wider workflow and operational system support

### Possible future tools
- `devdata`
- `devview`
- `devhub`
- `devai`
- `devpkg`

### v2.0 product meaning
ForgeStack becomes a **broader workflow and hub-oriented platform** rather than only an app generator.

---

## Immediate Next Milestones

### M1.5-H — Hardening and Release Prep
Current focus includes:

- packaging hardening
- test discovery hardening
- CLI help and wording polish
- docs consistency cleanup
- implementation summary docs
- release-prep refinement

### After M1.5-H
- stronger release polish
- clearer public documentation
- broader first-user onboarding
- future milestone selection based on platform priorities

### 2.0 plugin wave
Add broader platform-expansion plugins once the core and 1.5 lanes are stable.

Good 2.0 candidates:
- wider frontend target families
- deeper hub/device ecosystem
- broader microcontroller families
- richer platform-tooling separation

---

## Documentation Roadmap

### First pass
Update docs that define the current truth:
- README
- docs overview
- introduction
- CLI
- object model
- presets and projects
- current architecture

### Second pass
Update strategic docs:
- product strategy
- roadmap
- data-science strategy
- hardware strategy
- platform tools

### Third pass
Clean engine docs and reduce duplication:
- core engine
- graph engine
- planner
- executor
- validation and state
- plugin system
- architecture spec cleanup

---

## Product-Lane Roadmap

### Now
- preset-driven connected starter apps
- clear object model
- stable core path

### Near future
- data-science / technician / workflow tooling
- local-processing support
- SQLite-backed lightweight systems
- partial frontends

### Future future
- hub-oriented application patterns
- broader tool-family structure
- broader workflow ecosystems
- richer operational generation surfaces

---

## Summary

### v1.0
Stable core and connected generated starter app.

### v1.5
Workflow, technician, data, and lightweight-local expansion.

### v2.0
Broader platform and hub-oriented expansion.

The roadmap should keep ForgeStack grounded in what is already real while making room for the stronger broader platform that can grow from the same foundation.
