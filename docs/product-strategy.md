# Product Strategy

ForgeStack should be built in three strategic phases.

## Phase 1 — Compatibility Layer

First, ForgeStack should support the things developers already expect.

### Plugin categories

- Web app stack plugins
- Infrastructure plugins
- Observability plugins
- Dev workflow plugins

### Example v1 web stack

```yaml
plugins:
  - react
  - fastapi
  - postgres
  - redis
  - celery
```

Generated:

```text
frontend/
backend/
docker-compose.yml
.env
Makefile
```

This gives ForgeStack immediate practical value.

## Phase 2 — Ecosystem Layer

After the core is stable, ForgeStack should expand through plugins.

Targets:

- PyPI plugin discovery
- official plugin packages
- example stacks
- contributor-friendly plugin APIs

## Phase 3 — Category Creation

After trust is established, ForgeStack should pivot into spaces that are underserved.

### Data science platforms

```yaml
plugins:
  - jupyter
  - pandas
  - scikit-learn
  - postgres
  - airflow
  - fastapi
  - react_dashboard
```

Generated:

```text
notebooks/
data/
pipelines/
backend/
dashboard/
docker-compose.yml
```

### Device + backend systems

```yaml
plugins:
  - arduino
  - mqtt
  - fastapi
  - postgres
  - grafana
```

Generated:

```text
firmware/
edge/
backend/
dashboard/
docker-compose.yml
```

This is where ForgeStack becomes unique.
