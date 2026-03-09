from dataclasses import dataclass, field

@dataclass
class PluginMetadata:
    name: str
    requires: list[str] = field(default_factory=list)


class Plugin:

    def __init__(self, name, requires=None):

        self.name = name
        self.requires = requires or []

    def plan(self, ctx):
        raise NotImplementedError