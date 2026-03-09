import yaml

def render_compose_yaml(compose):
    compose.setdefault("version", "3.9")
    return yaml.safe_dump(compose, sort_keys=False)
