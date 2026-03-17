<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** [Prev: Lean Core Principles](lean-core-principles.md) | [Next: Hardware Strategy](hardware-strategy.md)  
> **Related:** [Platform Tools](platform-tools.md)

# Data Science Strategy

Data science is one of the strongest near-term strategic lanes for ForgeStack.

That does **not** mean ForgeStack should become a data-science-only product. It means data science, technician workflows, and internal operational tooling together form the clearest early wedge for the platform.

ForgeStack should remain general in architecture while becoming strongest first in this lane.

Its current active CLI is **`devmake`**.

---

## Why This Matters

Data science and technical workflow teams repeatedly rebuild the same kinds of environments:

- Python environments
- notebooks
- data storage
- orchestration layers
- serving layers
- dashboards
- processing pipelines
- worker systems
- backend APIs

That setup is often:

- repetitive
- fragile
- inconsistent across teams
- hard to document
- hard to reproduce

ForgeStack is well positioned to improve this because it already models generation through:

- stack presets
- app presets
- project objects
- dependency-aware plugins
- generated output

That makes it capable of generating not just projects, but repeatable technical working environments.

---

## Strategic Role of Data Science in ForgeStack

Data science should be treated as:

- a **strong early specialization**
- a **credible market wedge**
- a **bridge into technician and workflow tooling**

It should **not** be treated as the only future identity of ForgeStack.

The right balance is:

- broad platform
- strongest early lane in data science / technician / workflow tooling

This keeps the product flexible while still giving it a believable “master-of-one” direction.

---

## What Data Science Means Here

In ForgeStack, data science should be interpreted broadly.

It includes:

- notebook-based work
- data exploration
- reproducible environments
- pipeline workflows
- model-serving backends
- data-processing systems
- technician-side workbenches
- internal operations and analytics tooling

This broader interpretation is important.

ForgeStack should not be framed as only an ML experiment launcher. It should support the wider practical environment around data and technical workflows.

---

## Why ForgeStack Fits This Lane

ForgeStack already has structural qualities that fit this space well:

### 1. Reusable technical composition
Technical stacks can be reused through stack presets.

### 2. Reusable application intent
Different app or workflow archetypes can be represented through app presets.

### 3. Concrete project instantiation
Projects can select stack + app + overrides without redefining everything.

### 4. Dependency-aware generation
Plugins and execution planning already align with the needs of multi-part technical systems.

### 5. Workflow expansion path
The same model can later support:
- JupyterLab
- Voilà
- Kedro
- SQLite
- worker systems
- dashboards
- internal technician tools

This is why data science is a natural fit rather than an artificial add-on.

---

## Near-Term Data Science Priorities

The strongest near-term additions in this lane have centered on:

- **Jupyter / notebook workspace support**
- **Voilà**
- **Kedro**
- **SQLite**

These belong mainly in the **1.5 wave**. Much of this lane is now implemented in scaffold or vertical-slice form, with the current focus shifting toward hardening, polish, and release preparation.

### Why JupyterLab / Notebook
These provide technician and analyst workspaces.

### Why Voilà
This provides lightweight dashboard and notebook-to-view publishing capability.

### Why Kedro
This adds structured, pipeline-oriented workflow support.

### Why SQLite
This supports:
- lightweight local persistence
- staging
- local workflow tools
- processing-side metadata
- small operational installs

This makes SQLite especially relevant for local or technician-oriented systems.

---

## Recommended Plugin Direction

The data-science and workflow lane is now best understood as a staged implementation direction rather than a purely hypothetical candidate list.

### Environment and execution
- python
- conda or poetry later
- worker support

### Notebook and workspace
- jupyter
- notebook workspace support

### Data and storage
- postgres
- sqlite
- duckdb later if desired
- object storage later if needed

### Pipeline and orchestration
- kedro
- airflow / prefect / dagster later if justified

### Serving and integration
- fastapi
- celery
- redis

### Dashboard and operational view
- voila
- react-based frontends
- technician or analyst console presets

The important point is not to add everything immediately. It is to grow this lane in a staged and coherent way.

---

## Recommended Preset Direction

This lane is best expressed through **presets**, not just plugin lists.

### Implemented or strongly aligned stack presets
- `ml-stack`
- `data-workbench-stack`
- `local-workflow-stack`

### Implemented or strongly aligned app presets
- `datascience-dashboard`
- `technician-console`
- `data-workbench`
- `pipeline-workbench`

### Possible future additions
- `analysis-stack`
- `analysis-workbench`
- `workflow-monitor`
- `model-review-panel`

This keeps the product aligned with the current object model rather than falling back into a stack-only mindset.

---

## Role of SQLite in This Strategy

SQLite deserves special mention.

It should become a first-class ForgeStack option in this lane because it fits:

- local tools
- branch-side tools
- processing stages
- staging metadata
- lightweight operational installs
- technician-side applications

### Role split recommendation

#### PostgreSQL
Best for:
- central systems
- shared multi-user backends
- heavier persistent services

#### SQLite
Best for:
- local processing
- lightweight persistence
- temporary workflow state
- technician and operational tools

That split gives ForgeStack more practical range.

---

## Product Positioning Implication

The data-science lane should strengthen ForgeStack’s identity without narrowing it too much.

### Good positioning
ForgeStack helps generate:
- data-science workbenches
- analyst tools
- technician tools
- workflow and processing systems
- connected app backends around those workflows

### Less helpful positioning
ForgeStack is only for ML stacks or notebook users.

The product should stay broader than that.

---

## Relation to Technician and Workflow Strategy

This lane is closely related to technician and internal workflow tooling.

That is an advantage.

It means ForgeStack can support:

- analysts
- technical operators
- technicians
- internal process owners

without splitting into totally separate architectures.

That broader usefulness is one reason data science remains a strong early wedge.

---

## Version Guidance

### v1.0
Keep the core focused on:
- stable object model
- connected starter app
- strong generation path

Optional:
- a simple Jupyter sidecar only if low-risk

### v1.5
This is the main data-science expansion phase:
- JupyterLab / Notebook
- Voilà
- Kedro
- SQLite
- workflow-oriented presets
- technician-oriented presets

### v2.0
Broaden into richer platform behavior:
- more workflow orchestration
- stronger local/central patterns
- deeper tool-family separation if useful
- wider operational frontends

---

## Design Rule

ForgeStack should treat data science as a strong practical product lane built on top of the same core model:

- stack
- app
- project
- output

That means the platform should expand into data-science and technician workflows **through presets and plugins**, not by bending the core model into something special-case and brittle.

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** [Prev: Product Strategy](product-strategy.md) | [Next: Hardware Strategy](hardware-strategy.md)  
**Related:** [Platform Tools](platform-tools.md)
