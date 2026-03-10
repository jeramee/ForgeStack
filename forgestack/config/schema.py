# forgestack/config/schema.py

VALID_KINDS = {
    "stack",
    "stack-legacy",
    "app",
    "project",
    "resolved-project",
}


REQUIRED_FIELDS = {
    "stack": {"name"},
    "app": {"name"},
    "project": {"name", "uses"},
    "resolved-project": {"name", "plugins", "stack", "app", "project", "values"},
}