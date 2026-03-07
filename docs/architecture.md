# Architecture Overview

ForgeStack follows a modular architecture:

CLI
→ Config Loader
→ Plugin Registry
→ Dependency Resolver
→ Dependency Graph
→ Planner
→ Executor
→ State Store

The goal is a **small core with a large plugin ecosystem**.