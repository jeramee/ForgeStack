APP_CONFIG = {
    "project_name": "{{ project_name }}",
    "stack_name": "{{ stack.get('name', '') }}",
    "app_name": "{{ app.get('name', '') }}",
    "features": {
{% for name, enabled in features.items() %}
        "{{ name }}": {{ "True" if enabled else "False" }}{% if not loop.last %},{% endif %}
{% endfor %}
    },
{% if has_plugin.get("redis") %}
    "redis": {
        "host": "redis",
        "port": {{ values.get('redis', {}).get('port', 6379) }},
    },
{% endif %}
{% if has_plugin.get("postgres") %}
    "postgres": {
        "host": "postgres",
        "port": {{ values.get('postgres', {}).get('port', 5432) }},
        "database": "{{ values.get('postgres', {}).get('db', 'app') }}",
    },
{% endif %}

{% if has_plugin.get("jupyter") %}
    "jupyter": {
        "enabled": True,
        "port": {{ values.get('jupyter', {}).get('port', 8888) }},
    },
{% endif %}

{% if has_plugin.get("kedro") %}
    "workflow": {
        "enabled": True,
        "engine": "kedro",
        "pipeline_root": "pipelines",
        "config_root": "conf",
        "data_root": "data",
    },
{% endif %}

{% if has_plugin.get("voila") %}
    "voila": {
        "enabled": True,
        "port": {{ values.get('voila', {}).get('port', 8866) }},
    },
{% endif %}

{% if has_plugin.get("sqlite") %}
    "sqlite": {
        "enabled": {{ "True" if has_plugin.get("sqlite") else "False" }},
        "database": "{{ values.get('sqlite', {}).get('database', 'app.db') }}",
    },
{% endif %}
}