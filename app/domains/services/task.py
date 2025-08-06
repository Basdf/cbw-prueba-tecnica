from app.domains.models.task import (
    CreateTaskRequest,
    PatchTaskRequest,
    PutTaskRequest,
    TaskResponse,
    TaskStatus,
)
from app.domains.ports.task import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def get_all_tasks(self) -> list[TaskResponse]:
        return self.repository.get_all()

    async def get_task_by_id(self, id: str) -> TaskResponse:
        return self.repository.get_by_id(id)

    async def get_tasks_by_status(self, status: TaskStatus) -> list[TaskResponse]:
        return self.repository.get_by_status(status)

    async def create_task(self, new_task: CreateTaskRequest) -> TaskResponse:
        return self.repository.create(new_task)

    async def update_task(self, id: str, put_task: PutTaskRequest) -> TaskResponse:
        return self.repository.update(id, put_task)

    async def patch_task(self, id: str, patch_task: PatchTaskRequest) -> TaskResponse:
        return self.repository.patch(id, patch_task)

    async def delete_task(self, id: str) -> None:
        self.repository.delete(id)
