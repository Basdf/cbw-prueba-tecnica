from pydantic_extra_types.mongo_object_id import MongoObjectId
from pymongo.asynchronous.collection import AsyncCollection

from app.configs.logging import get_logging
from app.configs.mongo import MongoDBConfig
from app.domains.models.task import (
    CreateTask,
    PatchTask,
    PutTask,
    TaskFilter,
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

    async def get_all(self, payload: TaskFilter) -> list[TaskResponse]:
        cursor = self.collection.find(
            payload.model_dump(exclude_none=True, by_alias=True)
        )
        return [TaskResponse(**task) async for task in cursor]

    async def get_by_id(self, id: MongoObjectId) -> TaskResponse:
        return await self.collection.find_one({"_id": id})

    async def get_by_status(self, status: TaskStatus) -> list[TaskResponse]:
        cursor = self.collection.find({"status": status})
        return [TaskResponse(**task) async for task in cursor]

    async def create(self, new_task: CreateTask) -> TaskResponse:
        task_insert_response = await self.collection.insert_one(new_task.model_dump())
        return await self.get_by_id(task_insert_response.inserted_id)

    async def update(self, id: MongoObjectId, put_task: PutTask) -> TaskResponse:
        put_task_json = put_task.model_dump()
        await self.collection.update_one(
            {"_id": id},
            {"$set": put_task_json},
        )
        return await self.get_by_id(id)

    async def patch(self, id: MongoObjectId, patch_task: PatchTask) -> TaskResponse:
        patch_task_json = patch_task.model_dump(exclude_none=True)
        await self.collection.update_one(
            {"_id": id},
            {"$set": patch_task_json},
        )
        return await self.get_by_id(id)

    async def delete(self, id: MongoObjectId) -> None:
        await self.collection.delete_one({"_id": id})
        return None
