import asyncio

from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.adapters.repositories.mongo.task import TaskMongoRepository
from app.configs.celery import celery_app
from app.configs.logging import get_logging
from app.configs.mongo import MongoDBConfig
from app.configs.settings import settings

log = get_logging(__name__)


@celery_app.task(
    name="review_task_status",
    queue="review_queue",
    pydantic=True,
)
def review_task_status(id: str) -> None:
    async def run():
        await asyncio.sleep(10)
        mongo_db = MongoDBConfig(uri=settings.MONGO_URI, db_name=settings.MONGO_DB_NAME)
        task_repo = TaskMongoRepository(mongo_db=mongo_db)
        object_id = MongoObjectId.validate(id)
        task = await task_repo.get_by_id(object_id)
        log.info(f"Found task for report: {task.id}")
        log.info(
            f"Task ID: {task.id}, Status: {task.status}, Assigned To: {task.assigned_to}"
        )

    log.info("Starting review_task_status")
    asyncio.run(run())
    log.info("Completed review_task_status")
