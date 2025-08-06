from abc import ABC, abstractmethod

from app.domains.models.task import (
    CreateTaskRequest,
    PatchTaskRequest,
    PutTaskRequest,
    TaskResponse,
    TaskStatus,
)


class TaskRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[TaskResponse]:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> TaskResponse:
        pass

    @abstractmethod
    async def get_by_status(self, status: TaskStatus) -> list[TaskResponse]:
        pass

    @abstractmethod
    async def create(self, new_task: CreateTaskRequest) -> TaskResponse:
        pass

    @abstractmethod
    async def update(self, id: str, put_task: PutTaskRequest) -> TaskResponse:
        pass

    @abstractmethod
    async def patch(self, id: str, patch_task: PatchTaskRequest) -> TaskResponse:
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        pass
