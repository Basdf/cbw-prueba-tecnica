from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.configs.celery import celery_app
from app.configs.logging import get_logging

log = get_logging(__name__)


@celery_app.task(
    name="review_task_status",
    queue="review_queue",
    pydantic=True,
)
def review_task_status(id: MongoObjectId) -> None:
    log.info(f"Reviewing status for task ID: {id}")
    pass
