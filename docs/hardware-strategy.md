# Hardware and Device Strategy

ForgeStack should eventually support device + backend scaffolding.

## Why this is interesting

Very few developer tools scaffold end-to-end systems that include:

- firmware
- messaging
- backend APIs
- storage
- monitoring

## Example stack

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

## Design rule

ForgeStack should not become an embedded framework.

It should orchestrate hardware toolchains the same way it orchestrates web and DS stacks.

That means:

- Arduino is a plugin
- PlatformIO is a plugin
- MQTT is a plugin
- Grafana is a plugin

The core only wires the system together.
