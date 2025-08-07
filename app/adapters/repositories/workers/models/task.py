from datetime import datetime

from pydantic import BaseModel, Field

from app.domains.models.task import TaskStatus


class TaskReport(BaseModel):
    status: list[TaskStatus] | None = Field(None)
    assigned_to: str | None = Field(None)
    init_date: datetime = Field(...)
    end_date: datetime = Field(...)
