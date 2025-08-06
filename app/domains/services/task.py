from app.domains.models.task import (
    CreateTask,
    CreateTaskRequest,
    PatchTask,
    PatchTaskRequest,
    PutTask,
    PutTaskRequest,
    TaskResponse,
    TaskStatus,
)
from app.domains.ports.task import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def get_all_tasks(self) -> list[TaskResponse]:
        return await self.repository.get_all()

    async def get_task_by_id(self, id: str) -> TaskResponse:
        return await self.repository.get_by_id(id)

    async def get_tasks_by_status(self, status: TaskStatus) -> list[TaskResponse]:
        return await self.repository.get_by_status(status)

    async def create_task(self, new_task: CreateTaskRequest) -> TaskResponse:
        return await self.repository.create(CreateTask(**new_task.model_dump()))

    async def update_task(self, id: str, put_task: PutTaskRequest) -> TaskResponse:
        return await self.repository.update(id, PutTask(**put_task.model_dump()))

    async def patch_task(self, id: str, patch_task: PatchTaskRequest) -> TaskResponse:
        return await self.repository.patch(id, PatchTask(**patch_task.model_dump()))

    async def delete_task(self, id: str) -> None:
        await self.repository.delete(id)
