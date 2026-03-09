import yaml


def load_stack_yaml(path):
    """
    Load stack.yaml and return plugin list.

    Example stack.yaml:

    plugins:
      - fastapi
      - postgres
    """

    with open(path, "r") as f:
        data = yaml.safe_load(f)

    plugins = data.get("plugins", [])

    if not isinstance(plugins, list):
        raise ValueError("stack.yaml 'plugins' must be a list")

    return plugins