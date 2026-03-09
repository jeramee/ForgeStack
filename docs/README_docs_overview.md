# ForgeStack Documentation Overview

This documentation set reflects the current ForgeStack direction:

- **Terraform for development stacks**
- **Nx for project graphs**
- **Cookiecutter for scaffolding**

ForgeStack is a **lean orchestration core** with a **plugin ecosystem**.

The core is responsible for:

- config loading
- plugin discovery
- dependency resolution
- graph construction
- planning
- execution
- validation
- state

Everything else is a plugin:

- web frameworks
- databases
- cloud integrations
- observability
- data science tools
- hardware toolchains

## Strategic Direction

ForgeStack follows a three-phase product strategy:

1. **Compatibility Layer**  
   Match the developer experience people already expect from web and infra tooling.

2. **Ecosystem Layer**  
   Expand through official and third-party plugins.

3. **Category Creation**  
   Pivot hard into:
   - Data science platform scaffolding
   - Device + backend scaffolding

## Golden Rule

ForgeStack should never become a platform that *runs everything*.

ForgeStack should become a system that *wires everything*.
