from datetime import date, datetime
from typing import TypeVar

from pydantic import BaseModel, ConfigDict, Field

from app.domains.models.task import TaskStatus

T = TypeVar("T")


class DateTimeRange(BaseModel):
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)
    start: datetime | None = Field(None, alias="$gte")
    end: datetime | None = Field(None, alias="$lte")


class InListFilter[T](BaseModel):
    model_config = ConfigDict(validate_by_name=True)
    values: list[T] | None = Field(None, alias="$in")


class CreateTask(BaseModel):
    title: str = Field(...)
    description: str | None = Field(None)
    status: TaskStatus = Field(...)
    assigned_to: str | None = Field(None)
    due_date: datetime | None = Field(None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(None)


class PatchTask(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    status: TaskStatus | None = Field(None)
    assigned_to: str | None = Field(None)
    due_date: datetime | None = Field(None)
    updated_at: datetime = Field(default_factory=datetime.now)


class TaskFilter(BaseModel):
    def __init__(
        self,
        title: str | None = None,
        description: str | None = None,
        status: list[TaskStatus] | None = None,
        assigned_to: str | None = None,
        due_date_init_date: date | None = None,
        due_date_end_date: date | None = None,
        created_at_init_date: date | None = None,
        created_at_end_date: date | None = None,
    ):
        super().__init__()
        self.title = title
        self.description = description
        self.status = InListFilter[TaskStatus](values=status) if status else None
        self.assigned_to = assigned_to
        if due_date_init_date or due_date_end_date:
            self.due_date = DateTimeRange(
                start=due_date_init_date,
                end=datetime.combine(
                    due_date_end_date,
                    datetime.max.time(),
                )
                if due_date_end_date
                else None,
            )
        if created_at_init_date or created_at_end_date:
            self.created_at = DateTimeRange(
                start=created_at_init_date,
                end=datetime.combine(
                    created_at_end_date,
                    datetime.max.time(),
                )
                if created_at_end_date
                else None,
            )

    title: str | None = Field(None)
    description: str | None = Field(None)
    status: InListFilter[TaskStatus] | None = Field(None)
    assigned_to: str | None = Field(None)
    due_date: DateTimeRange | None = Field(None)
    created_at: DateTimeRange | None = Field(None)
