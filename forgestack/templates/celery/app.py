from celery import Celery

REDIS_HOST = "redis"
REDIS_PORT = {{ values.get('redis', {}).get('port', 6379) }}
BROKER_URL = "{{ values.get('celery', {}).get('broker_url') or ('redis://redis:' ~ values.get('redis', {}).get('port', 6379) ~ '/0') }}"

celery_app = Celery(
    "tasks",
    broker=BROKER_URL,
    backend=BROKER_URL,
    include=["tasks"],
)
