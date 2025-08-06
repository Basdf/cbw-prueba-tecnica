from fastapi import APIRouter

from app.adapters.controllers.task import router as task_router

api_router = APIRouter()
api_router.include_router(task_router, prefix="/v1/tasks", tags=["Tasks"])
