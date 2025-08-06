from datetime import datetime

from app.config.logging import get_logging
from app.domains.models.task import (
    CreateTaskRequest,
    PatchTaskRequest,
    PutTaskRequest,
    TaskResponse,
    TaskStatus,
)
from app.domains.ports.task import TaskRepository

log = get_logging(__name__)


class TaskMongoRepository(TaskRepository):
    async def get_all(self) -> list[TaskResponse]:
        return []

    async def get_by_id(self, id: str) -> TaskResponse:
        return TaskResponse(
            id=id,
            title="Sample Task",
            description="This is a sample task description.",
            status=TaskStatus.PENDING,
            assigned_to=None,
            due_date=None,
            created_at=datetime.now().isoformat(),
            updated_at=None,
        )

    async def get_by_status(self, status: TaskStatus) -> list[TaskResponse]:
        return [
            TaskResponse(
                id="1",
                title="Sample Task",
                description="This is a sample task description.",
                status=status,
                assigned_to=None,
                due_date=None,
                created_at=datetime.now().isoformat(),
                updated_at=None,
            )
        ]

    async def create(self, new_task: CreateTaskRequest) -> TaskResponse:
        return TaskResponse(
            id="new_task_id",
            title=new_task.title,
            description=new_task.description,
            status=new_task.status,
            assigned_to=new_task.assigned_to,
            due_date=new_task.due_date,
            created_at=datetime.now().isoformat(),
            updated_at=None,
        )

    async def update(self, id: str, put_task: PutTaskRequest) -> TaskResponse:
        return TaskResponse(
            id=id,
            title=put_task.title,
            description=put_task.description,
            status=put_task.status,
            assigned_to=put_task.assigned_to,
            due_date=put_task.due_date,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )

    async def patch(self, id: str, patch_task: PatchTaskRequest) -> TaskResponse:
        return TaskResponse(
            id=id,
            title=patch_task.title or "Updated Task",
            description=patch_task.description or "Updated Description",
            status=patch_task.status or TaskStatus.PENDING,
            assigned_to=patch_task.assigned_to,
            due_date=patch_task.due_date,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )

    async def delete(self, id: str) -> None:
        log.info(f"Task with id {id} deleted successfully.")
        return None
