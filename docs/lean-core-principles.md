<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** [Next: Data Science Strategy](data-science-strategy.md)  
> **Related:** [Core Engine](core-engine.md)

# Lean Core Principles

ForgeStack should remain efficient and maintainable by following strict architectural rules.

---

## Core rule

Treat **all external systems as plugins**.

That includes:

- Docker
- Kubernetes
- cloud providers
- ML frameworks
- hardware toolchains

## Plugin isolation rule

Plugins may depend on heavy libraries.

Examples:

- `forgestack-plugin-kubernetes` → kubernetes SDK
- `forgestack-plugin-pytorch` → torch
- `forgestack-plugin-arduino` → platformio or arduino-cli wrappers

The core must never import those dependencies.

## Correct pattern

Good:

```python
class KubernetesPlugin(Plugin):
    def plan(self, ctx):
        ctx.create_file("k8s/deployment.yaml", "...")
```

Bad:

```python
# core package imports kubernetes and calls cluster APIs directly
```

## Optional tool execution

If a plugin wants to run commands like:

- `kubectl apply`
- `terraform apply`
- `platformio run`

those should be optional actions, not core requirements.

Users should be able to disable command execution:

```bash
forgestack apply --skip-commands
```

## Dependency philosophy

Keep core dependencies minimal:

- PyYAML
- rich (optional)
- pydantic or jsonschema (optional)
- networkx (optional)

No heavyweight platform dependencies in the core.

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** [Next: Product Strategy](product-strategy.md)  
**Related:** [Core Engine](core-engine.md)
