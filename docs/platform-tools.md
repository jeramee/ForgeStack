# Platform Tools

ForgeStack should be understood as a **platform**, not just a single CLI.

Its current active tool is **`devmake`**.

This document explains how the broader ForgeStack tool-family idea fits the current architecture, what is active now, and what belongs to the future roadmap.

---

## Core Idea

### ForgeStack = platform
ForgeStack is the umbrella platform and product family.

### `devmake` = current active tool
`devmake` is the active generation CLI that currently drives the project.

It is the real working tool today, and all current public-facing workflows should be documented around it.

### Future tools = planned platform expansion
Additional tools may later appear under the ForgeStack platform as the product broadens into:

- workflow systems
- technician tools
- analytics workspaces
- operator views
- hub-oriented coordination tools
- plugin and ecosystem tooling

These future tools should be treated as **planned platform tools**, not as if they are already fully active products.

---

## Why a Tool Family Makes Sense

ForgeStack is already growing beyond a narrow scaffold command.

The platform now includes or implies:

- preset discovery
- project creation
- dependency graphing
- planning
- generation
- future workflow tooling
- future operational tooling
- future hub-oriented coordination

As the platform expands, it is reasonable that not every capability belongs inside one CLI forever.

That is why the multi-tool idea still makes sense.

---

## Current Tool: `devmake`

### Role
`devmake` is the current generator CLI for ForgeStack.

### Current responsibility
It handles the main generation flow:

- list plugins
- list presets
- create project
- view dependency graph
- view execution plan
- apply generation

### Current command family

```powershell
devmake plugins
devmake presets list
devmake create project MyApp --stack web-stack --app finance-dashboard
devmake graph projects/MyApp.yaml
devmake plan projects/MyApp.yaml
devmake apply projects/MyApp.yaml
```

### Why it matters
`devmake` is the command that proves the current ForgeStack architecture is real.

Right now, it should remain the center of active implementation, documentation, and trust-building.

---

## Planned Tool Family

These are the major planned platform tools that fit the current ForgeStack direction.

They are not all active today, but they are useful names and roles to reserve in the platform model.

---

## `devdata`

### Intended role
Data, ingestion, processing, and technician-oriented workflow tooling.

### Best interpretation
`devdata` should not be limited to “data science” in a narrow ML sense.

It should cover a broader lane including:

- analytics workspaces
- notebook-oriented workflows
- ingestion pipelines
- transformation workflows
- processing-side tooling
- technician data operations
- local or staging workflows

### Likely future scope
- JupyterLab / Notebook support
- Voilà-linked views
- Kedro and pipeline workflows
- local workflow data tools
- SQLite-backed staging and operational utilities
- internal technical workbenches

### Recommended timing
Conceptually justified in **1.5** and beyond, but not yet a standalone active CLI.

---

## `devview`

### Intended role
Visualization, dashboards, monitoring, operational views, and partial frontends.

### Best interpretation
`devview` should be broader than “charts.”

It should cover:

- dashboards
- queue views
- operator panels
- technician panels
- monitoring screens
- status views
- partial frontends
- lightweight operational interfaces

### Likely future scope
- dashboard generation helpers
- workflow views
- monitoring or operator-facing surfaces
- partial frontend patterns
- maybe stronger notebook-to-view publishing later

### Recommended timing
Conceptually justified in **1.5** and beyond, but not yet a standalone active CLI.

---

## `devhub`

### Intended role
Hub-oriented coordination and later operational orchestration.

### Best interpretation
`devhub` is likely the strongest future tool after `devmake`.

It aligns with the longer-term direction of ForgeStack into:

- hub-oriented applications
- workflow coordination
- local/central processing patterns
- device and business-system coordination
- operator and technician control surfaces

### Likely future scope
- local/central service coordination
- operational topology helpers
- hub-facing runtime coordination
- future business-device control patterns

### Recommended timing
Mainly **2.0**, though the architectural concept should influence earlier design decisions.

---

## `devai`

### Intended role
AI-assisted development and workflow support.

### Best interpretation
`devai` would cover future AI-assisted features around:

- generation assistance
- workflow assistance
- code review or planning help
- future agentic capabilities
- AI-linked technical operations

### Recommended timing
Mostly **later**, likely **1.5 to 2.0** depending on how the platform evolves.

This should not distract from the current core product path.

---

## `devpkg`

### Intended role
Plugin, preset, template, or ecosystem package management.

### Best interpretation
`devpkg` becomes useful when ForgeStack has a mature enough ecosystem that package and plugin lifecycle management deserve their own surface.

That could include:
- plugin package discovery
- preset packs
- template packs
- compatibility checks
- ecosystem management utilities

### Recommended timing
Mostly **2.0** or later.

It is more valuable once the ecosystem is broader.

---

## Platform vs Tooling Rule

A very important rule is:

### Do not split implementation too early.

The platform can have multiple future tool identities **without fragmenting the current codebase prematurely**.

That means:

- reserve names and roles if useful
- document the tool-family direction clearly
- keep active implementation centered in the main ForgeStack repository for now
- avoid moving engineering effort into many thin repos too early

This helps maintain focus while still locking in the broader platform vision.

---

## Relationship to the Current Architecture

The future tool-family idea should remain compatible with the current canonical object model:

- stack
- app
- project
- output

It should also remain compatible with the current repository model:

```text
presets/
  stack/
  app/

projects/

output/

forgestack/
  templates/
```

That means future tools should extend the platform **through the same architecture**, not by inventing a competing model.

---

## Relationship to Product Strategy

The tool-family direction aligns with the broader phased roadmap.

### v1.0
- `devmake` is the active core tool
- platform identity exists, but tool-family expansion remains mostly conceptual

### v1.5
- stronger justification for `devdata` and `devview`
- workflow, technician, and partial-frontend lanes become more concrete

### v2.0
- stronger case for `devhub`
- stronger case for broader platform-tool separation
- richer ecosystem may justify `devpkg`
- broader AI or automation direction may justify `devai`

This is the right order because it keeps the platform credible.

---

## Recommended Positioning

A good working platform statement is:

### ForgeStack is the platform. `devmake` is the current active generator tool. Additional ForgeStack tools may later expand the platform into data, view, hub, AI, and ecosystem-management lanes.

That keeps the story clear without overstating current maturity.

---

## Current Documentation Rule

The documentation should:

- document `devmake` as the active public CLI now
- document future tools as planned platform directions
- avoid presenting those future tools as if they are already shipping
- keep the platform story coherent with the current roadmap

This avoids confusion and keeps the product trustworthy.

---

## Design Rule

The ForgeStack platform may eventually contain multiple tools, but the architecture should remain unified.

That means:

- one platform
- one core object model
- one consistent preset/project/output structure
- one staged roadmap
- multiple tools only when the product is ready for them

For now, that means:

### ForgeStack = platform  
### `devmake` = active tool  
### future tools = planned expansion, not current standalone public tools
