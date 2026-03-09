class Plan:
    def __init__(self):
        self.actions = []

    def add(self, action):
        self.actions.append(action)


def merge_plans(subplans):
    """
    Deterministically merge plugin subplans into one plan.
    """

    merged = Plan()

    # sort plugins for deterministic output
    for plugin_name in sorted(subplans):

        subplan = subplans[plugin_name]

        for action in subplan.actions:
            merged.add({
                "plugin": plugin_name,
                "action": action
            })

    return merged