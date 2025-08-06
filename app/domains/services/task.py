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

    def get_all_tasks(self) -> TaskResponse:
        return self.repository.get_all()

    def get_task_by_id(self, id: str) -> TaskResponse:
        return self.repository.get_by_id(id)

    def get_tasks_by_status(self, status: TaskStatus) -> TaskResponse:
        return self.repository.get_by_status(status)

    def create_task(self, new_task: CreateTaskRequest) -> TaskResponse:
        return self.repository.create(new_task)

    def update_task(self, id: str, put_task: PutTaskRequest) -> TaskResponse:
        return self.repository.update(id, put_task)

    def patch_task(self, id: str, patch_task: PatchTaskRequest) -> TaskResponse:
        return self.repository.patch(id, patch_task)

    def delete_task(self, id: str) -> None:
        self.repository.delete(id)
