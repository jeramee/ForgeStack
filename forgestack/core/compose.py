# NOTE:
# This module is part of a richer parallel composition path that is not the
# current authoritative public `devmake apply` path.
# Public generation behavior currently flows through:
# cli/main.py -> stack_loader.py -> preset_resolver.py -> registry.py
# -> planner.py -> plan_executor.py
# Keep new public apply behavior out of this module unless intentionally migrating.
import yaml

def render_compose_yaml(compose):
    compose.setdefault("version", "3.9")
    return yaml.safe_dump(compose, sort_keys=False)
