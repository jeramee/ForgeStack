# Graph Engine

ForgeStack maintains a dependency graph between plugins.

Example:

React → FastAPI → Postgres
            ↓
          Redis → Celery

The graph enables:

- ordering
- diagnostics
- visualization