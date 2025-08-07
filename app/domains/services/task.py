from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.configs.logging import get_logging
from app.domains.models.task import (
    AsyncTaskResponse,
    CreateTaskRequest,
    PatchTaskRequest,
    TaskFilterRequest,
    TaskReportRequest,
    TaskResponse,
    TaskStatus,
)
from app.domains.ports.task import TaskRepository, TaskWorker

log = get_logging(__name__)


class TaskService:
    def __init__(self, repository: TaskRepository, worker: TaskWorker):
        self.repository = repository
        self.worker = worker

    async def get_all_tasks(self, payload: TaskFilterRequest) -> list[TaskResponse]:
        return await self.repository.get_all(payload)

    async def get_task_by_id(self, id: MongoObjectId) -> TaskResponse:
        return await self.repository.get_by_id(id)

    async def get_tasks_by_status(self, status: TaskStatus) -> list[TaskResponse]:
        return await self.repository.get_by_status(status)

    async def create_task(self, new_task: CreateTaskRequest) -> TaskResponse:
        return await self.repository.create(new_task)

    async def update_task(
        self, id: MongoObjectId, put_task: CreateTaskRequest
    ) -> TaskResponse:
        return await self.repository.update(id, put_task)

    async def patch_task(
        self, id: MongoObjectId, patch_task: PatchTaskRequest
    ) -> TaskResponse:
        return await self.repository.patch(id, patch_task)

    async def delete_task(self, id: MongoObjectId) -> None:
        await self.repository.delete(id)

    def report_task(self, payload: TaskReportRequest) -> AsyncTaskResponse:
        return self.worker.report(payload)

    def review_task_status(self, id: MongoObjectId) -> AsyncTaskResponse:
        return self.worker.review_task_status(id)
