from app.configs.celery import celery_app
from app.configs.logging import get_logging
from app.domains.models.task import TaskReport

log = get_logging(__name__)


@celery_app.task(name="report", queue="report_queue", pydantic=True)
def report(payload: TaskReport) -> None:
    log.info(f"Reporting payload: {payload}")
    pass
