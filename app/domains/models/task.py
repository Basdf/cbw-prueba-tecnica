from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskResponse(BaseModel):
    id: str = Field(...)
    title: str = Field(...)
    description: str | None = Field(None)
    status: TaskStatus = Field(TaskStatus.PENDING)
    assigned_to: str | None = Field(None)
    due_date: date | None = Field(None)
    created_at: str = Field(...)
    updated_at: str | None = Field(None)


class CreateTaskRequest(BaseModel):
    title: str = Field(...)
    description: str | None = Field(None)
    status: TaskStatus = Field(TaskStatus.PENDING)
    assigned_to: str | None = Field(None)
    due_date: date | None = Field(None)


class PutTaskRequest(BaseModel):
    id: str = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    status: TaskStatus = Field(...)
    assigned_to: str = Field(...)
    due_date: date = Field(...)


class PatchTaskRequest(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    status: TaskStatus | None = Field(None)
    assigned_to: str | None = Field(None)
    due_date: date | None = Field(None)
