from abc import ABC, abstractmethod

from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.domains.models.task import (
    CreateTask,
    PatchTask,
    PutTask,
    TaskFilter,
    TaskReport,
    TaskResponse,
    TaskStatus,
)


class TaskRepository(ABC):
    @abstractmethod
    async def get_all(self, payload: TaskFilter) -> list[TaskResponse]:
        pass

    @abstractmethod
    async def get_by_id(self, id: MongoObjectId) -> TaskResponse:
        pass

    @abstractmethod
    async def get_by_status(self, status: TaskStatus) -> list[TaskResponse]:
        pass

    @abstractmethod
    async def create(self, new_task: CreateTask) -> TaskResponse:
        pass

    @abstractmethod
    async def update(self, id: MongoObjectId, put_task: PutTask) -> TaskResponse:
        pass

    @abstractmethod
    async def patch(self, id: MongoObjectId, patch_task: PatchTask) -> TaskResponse:
        pass

    @abstractmethod
    async def delete(self, id: MongoObjectId) -> None:
        pass


class TaskWorker(ABC):
    @abstractmethod
    def report(self, payload: TaskReport) -> str:
        pass

    @abstractmethod
    def review_task_status(self, id: MongoObjectId) -> str:
        pass
