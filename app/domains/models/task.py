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


class CreateTask(TaskConfig):
    title: str = Field(...)
    description: str | None = Field(None)
    status: TaskStatus = Field(TaskStatus.PENDING)
    assigned_to: str | None = Field(None)
    due_date: datetime | None = Field(None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(None)


class PutTaskRequest(TaskConfig):
    title: str = Field(...)
    description: str = Field(...)
    status: TaskStatus = Field(...)
    assigned_to: str = Field(...)
    due_date: date = Field(...)


class PutTask(TaskConfig):
    title: str = Field(...)
    description: str = Field(...)
    status: TaskStatus = Field(...)
    assigned_to: str = Field(...)
    due_date: datetime = Field(...)
    updated_at: datetime = Field(default_factory=datetime.now)


class PatchTaskRequest(TaskConfig):
    title: str | None = Field(None)
    description: str | None = Field(None)
    status: TaskStatus | None = Field(None)
    assigned_to: str | None = Field(None)
    due_date: date | None = Field(None)


class PatchTask(TaskConfig):
    title: str | None = Field(None)
    description: str | None = Field(None)
    status: TaskStatus | None = Field(None)
    assigned_to: str | None = Field(None)
    due_date: datetime | None = Field(None)
    updated_at: datetime = Field(default_factory=datetime.now)


class TaskFilterRequest(TaskConfig):
    title: str | None = Field(None)
    description: str | None = Field(None)
    status: TaskStatus | None = Field(None)
    assigned_to: str | None = Field(None)
    due_date_init_date: date | None = Field(None)
    due_date_end_date: date | None = Field(None)
    created_at_init_date: date | None = Field(None)
    created_at_end_date: date | None = Field(None)


class TaskFilter(TaskConfig):
    def __init__(
        self,
        title: str | None = None,
        description: str | None = None,
        status: TaskStatus | None = None,
        assigned_to: str | None = None,
        due_date_init_date: date | None = None,
        due_date_end_date: date | None = None,
        created_at_init_date: date | None = None,
        created_at_end_date: date | None = None,
    ):
        super().__init__()
        self.title = title
        self.description = description
        self.status = status
        self.assigned_to = assigned_to
        if due_date_init_date or due_date_end_date:
            self.due_date = DateTimeRange(
                start=due_date_init_date,
                end=due_date_end_date,
            )
        if created_at_init_date or created_at_end_date:
            self.created_at = DateTimeRange(
                start=created_at_init_date,
                end=created_at_end_date,
            )

    title: str | None = Field(None)
    description: str | None = Field(None)
    status: TaskStatus | None = Field(None)
    assigned_to: str | None = Field(None)
    due_date: DateTimeRange | None = Field(None)
    created_at: DateTimeRange | None = Field(None)


class TaskReportRequest(TaskConfig):
    status: list[TaskStatus] | None = Field(None)
    assigned_to: str | None = Field(None)
    init_date: datetime = Field(...)
    end_date: datetime = Field(...)


class TaskReport(TaskReportRequest): ...
