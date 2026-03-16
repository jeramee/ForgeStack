<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** [Prev: Introduction](introduction.md) | [Next: Current Architecture](current-architecture.md)  
> **Related:** [Architecture](architecture.md)

# ForgeStack Documentation Overview

This documentation set reflects the current ForgeStack direction.

ForgeStack is a modular platform for generating applications and workflow systems from composable presets and plugins.

Its current active CLI is **`devmake`**.

The project is now centered on a clearer object model than the older stack-only approach:

- **stack** = technical preset
- **app** = product or archetype preset
- **project** = concrete instance
- **output** = rendered filesystem result

This documentation is organized to match that direction.

---

## How to Read These Docs

If you are new to ForgeStack, start with the documents that explain the current model and current workflow first.

If you are working on the engine itself, the internal architecture and engine docs are the next layer.

If you are thinking about future positioning, tool-family growth, or roadmap planning, use the strategy documents last.

---

## Current Documentation Direction

ForgeStack documentation should reflect the current canonical project model, not the older mixed stack-only format.

That means documentation should consistently reflect:

- `devmake` as the current active CLI
- `presets/stack/`
- `presets/app/`
- `projects/`
- `output/`
- the stack/app/project/output object model
- the current connected generated full-stack app path

As the platform expands, future docs may describe additional tools, workflows, and product lanes, but those should build on top of the same core model rather than replace it.

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** [Prev: Introduction](introduction.md) | [Next: Current Architecture](current-architecture.md)  
**Related:** [Architecture](architecture.md)