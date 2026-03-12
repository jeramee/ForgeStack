APP_CONFIG = {
    "project_name": "{{ project_name }}",
    "stack_name": "{{ stack.get('name', '') if stack else '' }}",
    "app_name": "{{ app.get('name', '') if app else '' }}",
    "features": {{ features | tojson }},
    "redis": {
        "host": "redis",
        "port": {{ values.get('redis', {}).get('port', 6379) }},
    },
    "postgres": {
        "host": "postgres",
        "port": {{ values.get('postgres', {}).get('port', 5432) }},
        "db": "{{ values.get('postgres', {}).get('db', 'app') }}",
    },
}