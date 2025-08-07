from fastapi import APIRouter, Depends, Query, Request
from pydantic_extra_types.mongo_object_id import MongoObjectId

from app.domains.models.task import (
    CreateTaskRequest,
    PatchTaskRequest,
    PutTaskRequest,
    TaskFilterRequest,
    TaskReportRequest,
    TaskResponse,
    TaskStatus,
)
from app.domains.services.task import TaskService

router = APIRouter()


def get_task_service(request: Request) -> TaskService:
    return request.app.state.task_service


@router.get(
    "",
    response_model=list[TaskResponse],
    status_code=200,
    response_model_by_alias=False,
)
async def get_all(
    payload: TaskFilterRequest = Query(...),
    task_service: TaskService = Depends(get_task_service),
):
    return await task_service.get_all_tasks(payload)


@router.get(
    "/{id}",
    response_model=TaskResponse,
    status_code=200,
    response_model_by_alias=False,
)
async def get_by_id(
    id: MongoObjectId, task_service: TaskService = Depends(get_task_service)
):
    return await task_service.get_task_by_id(id)


@router.get(
    "/status/{status}",
    response_model=list[TaskResponse],
    status_code=200,
    response_model_by_alias=False,
)
async def get_by_status(
    status: TaskStatus, task_service: TaskService = Depends(get_task_service)
):
    return await task_service.get_tasks_by_status(status)


@router.post(
    "", response_model=TaskResponse, status_code=201, response_model_by_alias=False
)
async def create(
    new_task: CreateTaskRequest, task_service: TaskService = Depends(get_task_service)
):
    return await task_service.create_task(new_task)


@router.put(
    "/{id}", response_model=TaskResponse, status_code=200, response_model_by_alias=False
)
async def update(
    id: MongoObjectId,
    put_task: PutTaskRequest,
    task_service: TaskService = Depends(get_task_service),
):
    return await task_service.update_task(id, put_task)


@router.patch(
    "/{id}", response_model=TaskResponse, status_code=200, response_model_by_alias=False
)
async def patch(
    id: MongoObjectId,
    patch_task: PatchTaskRequest,
    task_service: TaskService = Depends(get_task_service),
):
    return await task_service.patch_task(id, patch_task)


@router.delete("/{id}", status_code=204)
async def delete(
    id: MongoObjectId, task_service: TaskService = Depends(get_task_service)
):
    await task_service.delete_task(id)
    return None


@router.post("/report", response_model=str, status_code=202)
async def report(
    task_report: TaskReportRequest,
    task_service: TaskService = Depends(get_task_service),
):
    return task_service.report_task(task_report)


@router.get("/review/{id}", response_model=str, status_code=202)
async def review(
    id: MongoObjectId, task_service: TaskService = Depends(get_task_service)
):
    return task_service.review_task_status(id)
