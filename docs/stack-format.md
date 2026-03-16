<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** [Prev: Presets and Projects](presets-and-projects.md) | [Next: Plugin System](plugin-system.md)  
> **Related:** [Current Architecture](current-architecture.md)

# Stack Format

The older stack-only format is no longer the main ForgeStack model.

ForgeStack now uses a broader object model built around:

- **stack presets**
- **app presets**
- **project objects**
- **output**

That means the platform is no longer best described only in terms of “a stack YAML file with plugins.”

---

## What Changed

Older ForgeStack documents centered on a single stack file such as:

```yaml
plugins:
  - react
  - fastapi
  - postgres
  - redis
  - celery
```

That model was useful early on, but it mixed together too many concerns.

ForgeStack now separates:

- reusable technical composition
- reusable product intent
- concrete project instances
- generated filesystem results

---

## Current Canonical Model

### Stack preset
Reusable technical composition.

### App preset
Reusable product or archetype composition.

### Project object
Concrete instance that selects a stack and an app.

### Output
Rendered filesystem result.

---

## Current Project Example

```yaml
kind: project
name: MyApp
uses:
  stack: web-stack
  app: finance-dashboard
overrides: {}
```

This project object is now the preferred input to:

```powershell
devmake graph projects/MyApp.yaml
devmake plan projects/MyApp.yaml
devmake apply projects/MyApp.yaml
```

---

## Where to Read Next

The older stack-only explanation has been superseded by these documents:

- [Object Model](object-model.md)
- [Presets and Projects](presets-and-projects.md)
- [CLI](cli.md)
- [Architecture](architecture.md)

These documents reflect the current ForgeStack direction.

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** [Prev: Presets and Projects](presets-and-projects.md) | [Next: Plugin System](plugin-system.md)  
**Related:** [Current Architecture](current-architecture.md)