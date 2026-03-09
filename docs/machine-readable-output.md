# Machine Readable Output

ForgeStack should support machine-readable outputs early.

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
