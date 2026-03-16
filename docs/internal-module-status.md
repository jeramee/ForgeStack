<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** [Prev: Contributing](contributing.md)  
> **Related:** [Current Architecture](current-architecture.md)

# Internal Module Status

## Active public path
- cli/main.py
- core/stack_loader.py
- core/preset_resolver.py
- core/registry.py
- core/planner.py
- core/plan_executor.py
- core/template_loader.py
- plugins/*
- templates/*
- presets/*
- projects/*

These define the current authoritative public `devmake` behavior.

## Shared but frozen
- core/models.py
- core/plugin_api.py

These support richer parallel seams but should not grow for public behavior unless the active public path is intentionally migrated.

## Parallel / quarantined
- core/composer.py
- core/executor.py
- core/plan.py

These belong to a richer parallel architecture and are not the current authoritative public apply path.

## Rule
Public behavior should improve in the active public path first.
Do not grow the frozen or quarantined seams unless intentionally migrating architecture.

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** [Prev: Contributing](contributing.md)  
**Related:** [Current Architecture](current-architecture.md)
