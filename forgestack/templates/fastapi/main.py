from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from celery.result import AsyncResult

from app_config import APP_CONFIG
from celery_app import celery_app
from tasks import ping

app = FastAPI(title="{{ project_name }}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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