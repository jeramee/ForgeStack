<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** [Prev: Architecture](architecture.md) | [Next: Roadmap](roadmap.md)  
> **Related:** [Presets and Projects](presets-and-projects.md)

# CLI

ForgeStack currently uses **`devmake`** as its active CLI.

This command-line interface is centered on a preset-driven workflow built around:

- stack presets
- app presets
- project objects
- generated output

The CLI should be understood as the operational surface for the current ForgeStack model, not the older single mixed stack-file model.

---

## Current Command Surface

Current supported command family:

```powershell
devmake plugins
devmake presets list
devmake create project MyApp --stack web-stack --app finance-dashboard
devmake graph projects/MyApp.yaml
devmake plan projects/MyApp.yaml
devmake apply projects/MyApp.yaml
```

These commands reflect the current canonical ForgeStack direction.

---

## Command Philosophy

ForgeStack should keep the near-term CLI explicit and readable.

The current preferred flow is:

1. discover presets
2. create a project
3. inspect graph
4. inspect plan
5. apply generation

This keeps project creation deliberate and makes the object model visible to the user.

---

## `devmake plugins`

Lists currently installed plugins.

### Example

```powershell
devmake plugins
```

### Purpose

This command is useful for:

- checking what the registry can discover
- confirming local plugin installation
- debugging environment or packaging issues

---

## `devmake presets list`

Lists available presets.

### Example

```powershell
devmake presets list
```

### Purpose

This is the discovery command for user-facing reusable objects.

It should expose the available:

- stack presets
- app presets

This is the preferred replacement for older examples-first discovery patterns.

---

## `devmake create project`

Creates a concrete project object from a stack preset and app preset.

### Recommended form

```powershell
devmake create project MyApp --stack web-stack --app finance-dashboard
```

### Result

This generates a project file such as:

```yaml
kind: project
name: MyApp
uses:
  stack: web-stack
  app: finance-dashboard
overrides: {}
```

### Why this matters

This command keeps project identity separate from preset identity.

For example:

- `web-stack` is a reusable technical preset
- `finance-dashboard` is a reusable app preset
- `MyApp` is the concrete generated project instance

That separation is one of the main design rules of ForgeStack.

---

## `devmake graph`

Builds and displays the dependency graph for a project file.

### Example

```powershell
devmake graph projects/MyApp.yaml
```

### Purpose

Shows the resolved plugin dependency structure before generation.

Useful for:

- understanding plugin relationships
- debugging dependency behavior
- validating graph construction
- explaining execution order

---

## `devmake plan`

Builds and displays the execution plan for a project file.

### Example

```powershell
devmake plan projects/MyApp.yaml
```

### Purpose

This is the preview step before generation.

ForgeStack follows a **plan-before-apply** rule. The planner should show what will happen before files are written.

Useful for:

- safety
- reproducibility
- debugging template and plugin behavior
- CI or future machine-readable output flows

---

## `devmake apply`

Executes the generation plan and writes output to the filesystem.

### Example

```powershell
devmake apply projects/MyApp.yaml
```

### Result

Generates output such as:

```text
output/MyApp/
```

Inside that generated folder, ForgeStack may create:

- frontend files
- backend files
- worker files
- Docker files
- environment files
- project documentation

---

## Recommended Near-Term Workflow

The recommended current workflow is:

```powershell
devmake presets list
devmake create project MyApp --stack web-stack --app finance-dashboard
devmake graph projects/MyApp.yaml
devmake plan projects/MyApp.yaml
devmake apply projects/MyApp.yaml
```

Then run the generated application:

```powershell
cd output\MyApp
docker compose up --build
```

---

## Project File Input

Today, the main input to graph, plan, and apply is a project definition file.

Example:

```yaml
kind: project
name: MyApp
uses:
  stack: web-stack
  app: finance-dashboard
overrides: {}
```

That means the CLI is already moving away from the older single mixed stack file model.

---

## Naming Rules

### Project names are user-facing
A project name should normally come from the user:

```powershell
devmake create project MyApp --stack web-stack --app finance-dashboard
```

### Preset names are reusable identities
Preset names are reusable references, not the same thing as the final project name.

This distinction helps ForgeStack scale cleanly.

---

## Near-Term CLI Direction

The near-term CLI should stay centered on explicit project creation.

### Preferred near-term shape
```powershell
devmake create project MyApp --stack web-stack --app finance-dashboard
```

### Current recommended apply form
```powershell
devmake apply projects/MyApp.yaml
```

### Possible future shorthand
```powershell
devmake apply MyApp
```
Or even this with alias enabled:
```powershell
dvmk apply MyApp
```

This shorthand is intentionally future-facing and is not the current documented public interface.

---

## Current Scope

The CLI should reflect what ForgeStack actually does now:

- discover plugins
- discover presets
- create project objects
- resolve dependencies
- display graphs
- display plans
- apply generation

It should not be documented as if older or future commands are already the active public interface unless they are clearly marked as future ideas.

---

## Design Rule

The CLI should stay aligned with the canonical object model:

- stack
- app
- project
- output

Commands should make those concepts clearer, not blur them back together.

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** [Prev: Architecture](architecture.md) | [Next: Roadmap](roadmap.md)  
**Related:** [Presets and Projects](presets-and-projects.md)