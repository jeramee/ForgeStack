
# ForgeStack Internal Architecture Specification

## Purpose

This document defines the internal architecture of ForgeStack.  
It is intended for core maintainers and contributors implementing or extending the ForgeStack engine.

ForgeStack is designed around a **small core with a large plugin ecosystem**.

The core is responsible only for:

- loading stack configuration
- discovering plugins
- resolving dependencies
- building a dependency graph
- generating a plan
- executing the plan
- reporting results

All domain-specific behavior belongs in plugins.

---

# Design Goals

ForgeStack follows several architectural principles.

### Small Core

The core engine should remain small and stable.

Responsibilities of the core:

- configuration parsing
- plugin discovery
- dependency resolution
- graph generation
- plan generation
- execution orchestration

### Plugin Driven

Plugins implement the actual behavior of the system:

- framework generators
- service integrations
- toolchain integrations
- template logic

### Plan Before Apply

All operations must support preview before execution.

```
forgestack plan
forgestack apply
```

This improves safety and reproducibility.

### Graph First

ForgeStack maintains an explicit dependency graph between plugins.

This allows:

- ordering
- visualization
- diagnostics
- future caching or parallelism

---

# High Level Architecture

```
CLI
 ↓
Config Loader
 ↓
Plugin Registry
 ↓
Dependency Resolver
 ↓
Dependency Graph
 ↓
Planner
 ↓
Executor
 ↓
State Store
 ↓
Output Renderer
```

Each stage performs one specific function.

---

# Repository Structure

Recommended repository layout:

```
forgestack/

  core/

    cli/
      main.py
      commands/

    config/
      loader.py
      schema.py
      models.py

    plugin_api/
      base.py
      context.py
      metadata.py

    registry/
      manager.py
      discovery.py

    graph/
      models.py
      builder.py
      sorter.py

    planner/
      planner.py
      actions.py
      plan.py
      validators.py

    executor/
      executor.py
      file_ops.py
      patch_ops.py

    state/
      models.py
      store.py

    output/
      console.py
      json.py

    utils/

  plugins/
  templates/
  examples/
  docs/
```

---

# Core Domain Models

## Stack Configuration

Stack configuration describes which plugins are active.

Example configuration:

```yaml
name: my_stack

plugins:
  - react
  - fastapi
  - postgres
  - redis
  - celery
```

### Python model

```python
from dataclasses import dataclass, field
from typing import Any

@dataclass
class StackConfig:
    name: str
    plugins: list[str]
    options: dict[str, Any] = field(default_factory=dict)
```

---

## Plugin Metadata

Plugins declare metadata describing their capabilities and dependencies.

```python
from dataclasses import dataclass, field

@dataclass
class PluginMetadata:
    name: str
    version: str
    requires: list[str] = field(default_factory=list)
    provides: list[str] = field(default_factory=list)
    description: str = ""
    compatible_core: str = ">=1.0.0"
```

---

## Dependency Graph

ForgeStack builds a directed graph representing plugin dependencies.

Example:

```
React → FastAPI → Postgres
            ↓
          Redis → Celery
```

Python model:

```python
@dataclass
class GraphNode:
    name: str
    plugin_name: str
    requires: list[str]

@dataclass
class DependencyGraph:
    nodes: dict[str, GraphNode]
    edges: dict[str, set[str]]
```

---

## Plan Model

A plan represents the set of actions ForgeStack will perform.

```python
from dataclasses import dataclass, field
from typing import Any

@dataclass
class PlanAction:
    kind: str
    path: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    description: str = ""
```

Plan container:

```python
@dataclass
class Plan:
    actions: list[PlanAction]
    warnings: list[str]
    diagnostics: list[str]
```

---

# Plugin Interface

Plugins implement a simple lifecycle interface.

```python
from abc import ABC

class Plugin(ABC):

    metadata: PluginMetadata

    def before_generate(self, ctx):
        pass

    def plan(self, ctx):
        pass

    def after_generate(self, ctx):
        pass
```

Plugins should **declare intent**, not perform filesystem operations directly.

---

# Plugin Context

Plugins interact with the planner through a context object.

Example interface:

```python
class PluginContext:

    def create_dir(self, path):
        pass

    def create_file(self, path, content):
        pass

    def update_file(self, path, content):
        pass

    def patch_file(self, path, pattern, replacement):
        pass

    def add_service(self, name, config):
        pass
```

This allows the planner to collect actions before execution.

---

# Dependency Resolution

Plugin dependencies are resolved before planning.

Example:

```
celery requires redis
```

Resolver algorithm:

1. Load requested plugins
2. Recursively load dependencies
3. Build graph
4. Topologically sort plugins

---

# Planner

The planner executes plugin planning hooks in dependency order.

Planner flow:

```
resolve dependencies
↓
build dependency graph
↓
topological sort
↓
run plugin planning hooks
↓
collect actions
↓
validate plan
```

Planner output:

```
Plan:

+ create directory: backend
+ create file: backend/main.py
+ add service: redis
```

---

# Executor

The executor applies the plan.

Example operations:

- create directories
- create files
- update files
- patch files
- write service definitions

Example executor loop:

```python
for action in plan.actions:

    if action.kind == "create_dir":
        mkdir()

    if action.kind == "create_file":
        write_file()

    if action.kind == "patch_file":
        patch_file()
```

---

# State Store

ForgeStack maintains minimal state for reproducibility.

Example file:

```
.forgestack/state.json
```

Example state:

```json
{
  "stack_name": "my_stack",
  "plan_hash": "abc123",
  "files": [
    {
      "path": "backend/main.py",
      "checksum": "sha256...",
      "plugin": "fastapi"
    }
  ]
}
```

This enables future commands:

```
forgestack diff
forgestack upgrade
```

---

# Execution Flow

## forgestack plan

```
CLI
→ load config
→ discover plugins
→ resolve dependencies
→ build graph
→ run planner
→ output plan
```

## forgestack apply

```
CLI
→ load config
→ build plan
→ execute actions
→ write state
```

---

# Example Plugin

FastAPI plugin example:

```python
class FastAPIPlugin(Plugin):

    metadata = PluginMetadata(
        name="fastapi",
        version="1.0",
        requires=[],
    )

    def plan(self, ctx):

        ctx.create_dir("backend")

        ctx.create_file(
            "backend/main.py",
            '''
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}
'''
        )
```

---

# Version Roadmap

## ForgeStack v1

Core platform features:

- CLI renamed to `forgestack`
- plugin interface stabilized
- dependency graph
- plan engine
- executor
- PyPI plugin discovery
- official core plugins
- example stacks

---

## ForgeStack v1.5

Lifecycle management features:

- `forgestack diff`
- `forgestack validate`
- `forgestack upgrade`
- plugin generator
- compatibility checks
- JSON plan output

---

## ForgeStack v2

Hardware + software stacks.

New plugins:

- arduino
- platformio
- esp32

Example stack:

```
arduino
mqtt
fastapi
postgres
```

Generated environment:

```
firmware/
backend/
dashboard/
```

Optional future GUI:

```
forgestack studio
```

---

# Design Rule

The governing rule of ForgeStack architecture:

**Core coordinates. Plugins declare. Executor applies.**

This separation allows the ForgeStack core to remain small while supporting a large ecosystem of plugins.
