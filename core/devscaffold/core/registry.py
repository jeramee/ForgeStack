from importlib.metadata import entry_points

registry = {}

def load_plugins(names):

    eps = entry_points(group="devscaffold.plugins")

    for ep in eps:
        registry[ep.name] = ep.load()

    missing = [n for n in names if n not in registry]

    if missing:
        raise RuntimeError(
            f"Missing plugins: {missing}. Installed: {sorted(registry.keys())}"
        )

    plugins = []

    for name in names:
        plugin = registry[name]()
        plugins.append(plugin)

    return plugins


def list_available_plugins():

    eps = entry_points(group="devscaffold.plugins")

    return sorted([ep.name for ep in eps])