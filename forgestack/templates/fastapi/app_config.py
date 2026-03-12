APP_CONFIG = {
    "project_name": "{{ project_name }}",
    "stack_name": "{{ raw.get('uses', {}).get('stack', '') if raw else '' }}",
    "app_name": "{{ raw.get('uses', {}).get('app', '') if raw else '' }}",
    "features": {
{% for name, enabled in features.items() %}
        "{{ name }}": {{ "True" if enabled else "False" }}{% if not loop.last %},{% endif %}
{% endfor %}
    },
    "redis": {
        "host": "redis",
        "port": {{ values.get('redis', {}).get('port', 6379) }},
    },
    "postgres": {
        "host": "postgres",
        "port": {{ values.get('postgres', {}).get('port', 5432) }},
        "database": "{{ values.get('postgres', {}).get('db', 'app') }}",
    },
}