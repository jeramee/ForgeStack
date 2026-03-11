APP_NAME = "{{ project_name }}"
POSTGRES_DB = "{{ values.get('postgres', {}).get('db', 'app_db') }}"
POSTGRES_PORT = {{ values.get('postgres', {}).get('port', 5432) }}
REDIS_PORT = {{ values.get('redis', {}).get('port', 6379) }}