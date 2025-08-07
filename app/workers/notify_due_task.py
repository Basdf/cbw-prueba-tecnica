from app.configs.celery import celery_app
from app.configs.logging import get_logging

log = get_logging(__name__)


@celery_app.task(
    name="notify_due_tasks",
    queue="notify_queue",
    pydantic=True
)
def notify_due_tasks() -> None:
    log.info("Notifying about due tasks.")
    pass
