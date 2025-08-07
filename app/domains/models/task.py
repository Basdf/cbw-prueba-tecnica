from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.mongo_object_id import MongoObjectId


class DateTimeRange(BaseModel):
    model_config: ConfigDict = ConfigDict(validate_by_alias=True, validate_by_name=True)
    start: datetime | None = Field(None, alias="$gte")
    end: datetime | None = Field(None, alias="$lte")


class TaskConfig(BaseModel):
    model_config: ConfigDict = ConfigDict(validate_by_alias=True, validate_by_name=True)


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskResponse(TaskConfig):
    id: MongoObjectId = Field(..., alias="_id")
    title: str = Field(...)
    description: str | None = Field(None)
    status: TaskStatus = Field(TaskStatus.PENDING)
    assigned_to: str | None = Field(None)
    due_date: date | None = Field(None)
    created_at: datetime = Field(...)
    updated_at: datetime | None = Field(None)


class CreateTaskRequest(TaskConfig):
    title: str = Field(...)
    description: str | None = Field(None)
    status: TaskStatus = Field(TaskStatus.PENDING)
    assigned_to: str | None = Field(None)
    due_date: date | None = Field(None)


class PutTaskRequest(TaskConfig):
    title: str = Field(...)
    description: str = Field(...)
    status: TaskStatus = Field(...)
    assigned_to: str = Field(...)
    due_date: date = Field(...)


class PatchTaskRequest(TaskConfig):
    title: str | None = Field(None)
    description: str | None = Field(None)
    status: TaskStatus | None = Field(None)
    assigned_to: str | None = Field(None)
    due_date: date | None = Field(None)


class TaskFilterRequest(TaskConfig):
    title: str | None = Field(None)
    description: str | None = Field(None)
    status: list[TaskStatus] | None = Field(None)
    assigned_to: str | None = Field(None)
    due_date_init_date: date | None = Field(None)
    due_date_end_date: date | None = Field(None)
    created_at_init_date: date | None = Field(None)
    created_at_end_date: date | None = Field(None)


class TaskReportRequest(TaskConfig):
    status: list[TaskStatus] | None = Field(None)
    assigned_to: str | None = Field(None)
    init_date: date = Field(...)
    end_date: date = Field(...)


class AsyncTaskResponse(TaskConfig):
    task_id: str = Field(...)
