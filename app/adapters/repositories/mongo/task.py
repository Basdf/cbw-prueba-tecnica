from pydantic_extra_types.mongo_object_id import MongoObjectId
from pymongo.asynchronous.collection import AsyncCollection

from app.adapters.repositories.mongo.models.task import (
    CreateTask,
    PatchTask,
    PutTask,
    TaskFilter,
)
from app.configs.logging import get_logging
from app.configs.mongo import MongoDBConfig
from app.domains.models.task import (
    CreateTaskRequest,
    PatchTaskRequest,
    PutTaskRequest,
    TaskFilterRequest,
    TaskResponse,
    TaskStatus,
)
from app.domains.ports.task import TaskRepository

log = get_logging(__name__)


class TaskMongoRepository(TaskRepository):
    mongo_db: MongoDBConfig
    collection: AsyncCollection

    def __init__(self, mongo_db: MongoDBConfig):
        self.mongo_db = mongo_db
        self.collection = self.mongo_db.get_collection("tasks")

    async def get_all(self, payload: TaskFilterRequest) -> list[TaskResponse]:
        query = TaskFilter(**payload.model_dump())
        cursor = self.collection.find(
            query.model_dump(exclude_none=True, by_alias=True)
        )
        return [TaskResponse(**task) async for task in cursor]

    async def get_by_id(self, id: MongoObjectId) -> TaskResponse:
        return await self.collection.find_one({"_id": id})

    async def get_by_status(self, status: TaskStatus) -> list[TaskResponse]:
        cursor = self.collection.find({"status": status})
        return [TaskResponse(**task) async for task in cursor]

    async def create(self, new_task: CreateTaskRequest) -> TaskResponse:
        document = CreateTask(**new_task.model_dump())
        task_insert_response = await self.collection.insert_one(
            document.model_dump(by_alias=True)
        )
        return await self.get_by_id(task_insert_response.inserted_id)

    async def update(self, id: MongoObjectId, put_task: PutTaskRequest) -> TaskResponse:
        query = PutTask(**put_task.model_dump())
        await self.collection.update_one(
            {"_id": id},
            {"$set": query.model_dump(by_alias=True)},
        )
        return await self.get_by_id(id)

    async def patch(
        self, id: MongoObjectId, patch_task: PatchTaskRequest
    ) -> TaskResponse:
        query = PatchTask(**patch_task.model_dump())
        await self.collection.update_one(
            {"_id": id},
            {"$set": query.model_dump(exclude_none=True, by_alias=True)},
        )
        return await self.get_by_id(id)

    async def delete(self, id: MongoObjectId) -> None:
        await self.collection.delete_one({"_id": id})
        return None
