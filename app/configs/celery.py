from celery import Celery
from celery.schedules import crontab

from app.configs.settings import settings

celery_app = Celery(
    "cbw_api",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
celery_app.conf.beat_schedule = {
    "notify-due-tasks-every-2-minutes": {
        "task": "notify_due_tasks",  # nombre registrado de la tarea
        "schedule": crontab(minute="*/2"),
    },
}
celery_app.conf.timezone = "UTC"
