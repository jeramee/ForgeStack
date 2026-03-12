from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
{% if has_plugin.get("celery") %}
from celery.result import AsyncResult
{% endif %}

from app_config import APP_CONFIG
{% if has_plugin.get("celery") %}
from celery_app import celery_app
from tasks import ping
{% endif %}
{% if has_plugin.get("sqlite") %}
from db import get_connection, init_db
{% endif %}

app = FastAPI(title="{{ project_name }}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

{% if has_plugin.get("sqlite") %}
@app.on_event("startup")
def startup_init_db():
    init_db()
{% endif %}


@app.get("/")
def root():
    return {"message": "{{ project_name }} backend is running"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "backend",
        "project": APP_CONFIG["project_name"],
    }


@app.get("/config")
def config():
    return APP_CONFIG


{% if has_plugin.get("celery") %}
@app.post("/tasks/ping")
def run_ping_task():
    task = ping.delay()
    return {
        "status": "queued",
        "task_id": task.id,
    }


@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    task = AsyncResult(task_id, app=celery_app)

    payload = {
        "task_id": task.id,
        "state": task.state,
        "ready": task.ready(),
        "successful": task.successful(),
    }

    if task.ready():
        if task.successful():
            payload["result"] = task.result
        else:
            payload["error"] = str(task.result)

    return payload
{% endif %}


{% if has_plugin.get("sqlite") %}
@app.get("/items")
def list_items():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT id, name FROM items ORDER BY id").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


@app.post("/items/seed")
def seed_item():
    conn = get_connection()
    try:
        conn.execute("INSERT INTO items (name) VALUES (?)", ("sample item",))
        conn.commit()
        return {"status": "ok"}
    finally:
        conn.close()
{% endif %}