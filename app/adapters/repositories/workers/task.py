from celery.result import AsyncResult
from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.adapters.repositories.workers.models.task import TaskReport
from app.configs.celery import celery_app
from app.configs.logging import get_logging
from app.domains.ports.task import TaskWorker

log = get_logging(__name__)


class TaskCeleryWorker(TaskWorker):
    def report(self, payload: TaskReport) -> str:
        result: AsyncResult = celery_app.send_task(
            "report", args=[payload.model_dump()], queue="report_queue"
        )
        return result.id

    def review_task_status(self, id: MongoObjectId) -> str:
        result: AsyncResult = celery_app.send_task(
            "review_task_status", args=[str(id)], queue="review_queue"
        )
        return result.id
