from fastapi import APIRouter

from app.adapters.repositories.task import TaskMongoRepository
from app.domains.models.task import (
    CreateTaskRequest,
    PatchTaskRequest,
    PutTaskRequest,
    TaskResponse,
    TaskStatus,
)
from app.domains.services.task import TaskService

router = APIRouter()
task_service = TaskService(TaskMongoRepository())


@router.get("", response_model=list[TaskResponse], status_code=200)
async def get_all():
    return await task_service.get_all_tasks()


@router.get("/{id}", response_model=TaskResponse, status_code=200)
async def get_by_id(id: str):
    return await task_service.get_task_by_id(id)


@router.get("/status/{status}", response_model=list[TaskResponse], status_code=200)
async def get_by_status(status: TaskStatus):
    return await task_service.get_tasks_by_status(status)


@router.post("", response_model=TaskResponse, status_code=201)
async def create(new_task: CreateTaskRequest):
    return await task_service.create_task(new_task)


@router.put("/{id}", response_model=TaskResponse, status_code=200)
async def update(id: str, put_task: PutTaskRequest):
    return await task_service.update_task(id, put_task)


@router.patch("/{id}", response_model=TaskResponse, status_code=200)
async def patch(id: str, patch_task: PatchTaskRequest):
    return await task_service.patch_task(id, patch_task)


@router.delete("/{id}", status_code=204)
async def delete(id: str):
    await task_service.delete_task(id)
    return None
