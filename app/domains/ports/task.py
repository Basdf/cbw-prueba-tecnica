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
    def get_all(self) -> TaskResponse:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> TaskResponse:
        pass

    @abstractmethod
    def get_by_status(self, status: TaskStatus) -> TaskResponse:
        pass

    @abstractmethod
    def create(self, new_task: CreateTaskRequest) -> TaskResponse:
        pass

    @abstractmethod
    def update(self, id: str, put_task: PutTaskRequest) -> TaskResponse:
        pass

    @abstractmethod
    def patch(self, id: str, patch_task: PatchTaskRequest) -> TaskResponse:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass
