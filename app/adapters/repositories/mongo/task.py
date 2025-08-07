from pydantic_extra_types.mongo_object_id import MongoObjectId
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.errors import PyMongoError

from app.adapters.repositories.mongo.models.task import (
    CreateTask,
    PatchTask,
    TaskFilter,
)
from app.configs.logging import get_logging
from app.configs.mongo import MongoDBConfig
from app.domains.models.errors import DatabaseError, NotFoundError
from app.domains.models.task import (
    CreateTaskRequest,
    PatchTaskRequest,
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
        try:
            query = TaskFilter(**payload.model_dump())
            cursor = self.collection.find(
                query.model_dump(exclude_none=True, by_alias=True)
            )
            return [TaskResponse(**task) async for task in cursor]
        except PyMongoError as e:
            log.error(f"Error getting all tasks: {e}")
            raise DatabaseError("Error getting all tasks")

    async def get_by_id(self, id: MongoObjectId) -> TaskResponse:
        try:
            response = await self.collection.find_one({"_id": id})
            if response is None:
                raise NotFoundError(f"Task with id {id} not found")
            return TaskResponse(**response)
        except PyMongoError as e:
            log.error(f"Error getting task by id {id}: {e}")
            raise DatabaseError("Error getting task by id")

    async def get_by_status(self, status: TaskStatus) -> list[TaskResponse]:
        try:
            cursor = self.collection.find({"status": status})
            return [TaskResponse(**task) async for task in cursor]
        except PyMongoError as e:
            log.error(f"Error getting tasks by status {status}: {e}")
            raise DatabaseError("Error getting tasks by status")

    async def create(self, new_task: CreateTaskRequest) -> TaskResponse:
        try:
            document = CreateTask(**new_task.model_dump())
            task_insert_response = await self.collection.insert_one(
                document.model_dump(by_alias=True)
            )
            return await self.get_by_id(task_insert_response.inserted_id)
        except PyMongoError as e:
            log.error(f"Error creating task: {e}")
            raise DatabaseError("Error creating task")

    async def update(
        self, id: MongoObjectId, put_task: CreateTaskRequest
    ) -> TaskResponse:
        try:
            query = CreateTask(**put_task.model_dump())
            await self.collection.update_one(
                {"_id": id}, {"$set": query.model_dump(by_alias=True)}, upsert=True
            )
            return await self.get_by_id(id)
        except PyMongoError as e:
            log.error(f"Error updating task {id}: {e}")
            raise DatabaseError("Error updating task")

    async def patch(
        self, id: MongoObjectId, patch_task: PatchTaskRequest
    ) -> TaskResponse:
        try:
            query = PatchTask(**patch_task.model_dump())
            response = await self.collection.update_one(
                {"_id": id},
                {"$set": query.model_dump(exclude_none=True, by_alias=True)},
            )
            if response.modified_count == 0:
                raise NotFoundError(f"Task with id {id} not found")
            return await self.get_by_id(id)
        except PyMongoError as e:
            log.error(f"Error patching task {id}: {e}")
            raise DatabaseError("Error patching task")

    async def delete(self, id: MongoObjectId) -> None:
        try:
            await self.collection.delete_one({"_id": id})
            return None
        except PyMongoError as e:
            log.error(f"Error deleting task {id}: {e}")
            raise DatabaseError("Error deleting task")
