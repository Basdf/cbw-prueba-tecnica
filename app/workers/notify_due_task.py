import asyncio
from datetime import date, timedelta

from app.adapters.repositories.mongo.task import TaskMongoRepository
from app.configs.celery import celery_app
from app.configs.logging import get_logging
from app.configs.mongo import MongoDBConfig
from app.configs.settings import settings
from app.domains.models.task import TaskFilterRequest, TaskStatus

log = get_logging(__name__)


@celery_app.task(name="notify_due_tasks", queue="notify_queue", pydantic=True)
def notify_due_tasks() -> None:
    async def run():
        mongo_db = MongoDBConfig(uri=settings.MONGO_URI, db_name=settings.MONGO_DB_NAME)
        task_repo = TaskMongoRepository(mongo_db=mongo_db)
        tasks = await task_repo.get_all(
            TaskFilterRequest(
                status=[TaskStatus.PENDING, TaskStatus.IN_PROGRESS],
                due_date_init_date=date.today() - timedelta(days=1),
                due_date_end_date=date.today() + timedelta(days=1),
            )
        )
        for task in tasks:
            log.info(f"Notifying user about due task: {task.id}")
        await mongo_db.close_connection()

    log.info("Starting task to notify due tasks")
    asyncio.run(run())
    log.info("Completed task to notify due tasks")
