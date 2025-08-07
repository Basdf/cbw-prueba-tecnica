from datetime import datetime, timedelta

from celery.result import AsyncResult
from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.configs.celery import celery_app
from app.configs.logging import get_logging
from app.domains.models.task import AsyncTaskResponse, TaskReportRequest
from app.domains.ports.task import TaskWorker

log = get_logging(__name__)


class TaskCeleryWorker(TaskWorker):
    def report(self, payload: TaskReportRequest) -> AsyncTaskResponse:
        result: AsyncResult = celery_app.send_task(
            name="report", args=payload.model_dump(), queue="report_queue"
        )
        return AsyncTaskResponse(task_id=str(result.id))

    def review_task_status(self, id: MongoObjectId) -> AsyncTaskResponse:
        result: AsyncResult = celery_app.send_task(
            name="review_task_status",
            args=[str(id)],
            queue="review_queue",
            eta=datetime.now() + timedelta(minutes=1),
        )
        return AsyncTaskResponse(task_id=str(result.id))
