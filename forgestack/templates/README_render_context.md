# Render Context Contract

Stable keys currently available to templates:

- `raw`
- `effective`
- `project`
- `project_name`
- `stack`
- `app`
- `values`
- `plugins`
- `has_plugin`
- `features`
- `has_feature`

## Rules

- Templates may depend on these keys.
- `features` is the normalized app feature mapping.
- `has_feature` is a convenience mapping for template conditionals.
- Filesystem target paths are renderer decisions, not schema concepts.
- App feature semantics should influence rendering through `features` / `has_feature`, not by leaking low-level plugin internals into preset docs.

## Template ID Convention

Canonical template IDs use namespaced logical identifiers such as:

- `react/package.json`
- `python/requirements.txt`
- `docker/postgres.yml`

Legacy flat template IDs may still be supported temporarily through aliases, but new work should use canonical namespaced IDs.