from celery import Celery

REDIS_HOST = "redis"
REDIS_PORT = {{ values.get('redis', {}).get('port', 6379) }}

celery_app = Celery(
    "tasks",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
)

celery_app.autodiscover_tasks()