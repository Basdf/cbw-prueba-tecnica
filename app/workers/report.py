import asyncio

from app.adapters.repositories.mongo.task import TaskMongoRepository
from app.configs.celery import celery_app
from app.configs.logging import get_logging
from app.configs.mongo import MongoDBConfig
from app.configs.settings import settings
from app.domains.models.task import TaskFilterRequest, TaskReportRequest

log = get_logging(__name__)


@celery_app.task(name="report", queue="report_queue", pydantic=True)
def report(payload: TaskReportRequest) -> None:
    async def run():
        await asyncio.sleep(10)
        mongo_db = MongoDBConfig(uri=settings.MONGO_URI, db_name=settings.MONGO_DB_NAME)
        task_repo = TaskMongoRepository(mongo_db=mongo_db)
        tasks = await task_repo.get_all(
            TaskFilterRequest(
                status=payload.status,
                assigned_to=payload.assigned_to,
                created_at_init_date=payload.init_date,
                created_at_end_date=payload.end_date,
            )
        )
        log.info(f"Found {len(tasks)} tasks for report")
        for task in tasks:
            log.info(
                f"Task ID: {task.id}, Status: {task.status}, Assigned To: {task.assigned_to}"
            )
        await mongo_db.close_connection()

    log.info("Starting report task")
    asyncio.run(run())
    log.info("Completed report task")
