<a id="top"></a>

> **Docs:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
> **Section:** [Prev: Validation and State](validation-and-state.md)  
> **Related:** [Platform Tools](platform-tools.md)

# Machine Readable Output

ForgeStack should support machine-readable outputs early.

---

## JSON plan output

```bash
forgestack plan --json
```

Example:

```json
{
  "actions": [
    {
      "kind": "create_dir",
      "path": "backend",
      "description": "Create backend app directory"
    },
    {
      "kind": "create_file",
      "path": "backend/main.py",
      "description": "Create FastAPI entrypoint"
    }
  ],
  "warnings": [],
  "diagnostics": []
}
```

## Why this matters

Machine-readable outputs enable:

- CI checks
- editor integrations
- future GUI work
- policy engines
- testing

---

**Navigation:** [README](../README.md) | [Docs Overview](README_docs_overview.md) | [Back to Top](#top)  
**Section:** [Prev: Validation and State](validation-and-state.md)  
**Related:** [Platform Tools](platform-tools.md)
