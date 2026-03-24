from celery import Celery
from src.config.config import settings

celery_app = Celery(
    "worker",
    broker= settings.BROKER,
    backend= settings.BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    imports=["src.worker.tasks"]
)