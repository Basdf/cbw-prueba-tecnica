from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.mongo_object_id import MongoObjectId

# Constantes para descripciones de campos
ID_DESC = "Unique identifier of the task"
TITLE_DESC = "Title of the task"
DESCRIPTION_DESC = "Description of the task"
STATUS_DESC = "Status of the task"
ASSIGNED_TO_DESC = "User assigned to the task"
DUE_DATE_DESC = "Due date of the task"
CREATED_AT_DESC = "Creation date of the task"
UPDATED_AT_DESC = "Last update date of the task"
INITIAL_DUE_DATE_DESC = "Initial due date"
END_DUE_DATE_DESC = "End due date"
INITIAL_CREATION_DATE_DESC = "Initial creation date"
END_CREATION_DATE_DESC = "End creation date"
REPORT_INIT_DATE_DESC = "Initial date for report"
REPORT_END_DATE_DESC = "End date for report"
CELERY_TASK_ID_DESC = "Celery task id"
START_DESC = "Start date-time for the range"
END_DESC = "End date-time for the range"


class DateTimeRange(BaseModel):
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)
    start: datetime | None = Field(
        None, alias="$gte", description=START_DESC, examples="2025-09-01T00:00:00"
    )
    end: datetime | None = Field(
        None, alias="$lte", description=END_DESC, examples="2025-09-30T23:59:59"
    )


class TaskConfig(BaseModel):
    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class IdField(BaseModel):
    id: MongoObjectId = Field(
        ..., description=ID_DESC, example="652e1f2b8f1c2a3d4e5f6a7b"
    )


class TitleField(BaseModel):
    title: str = Field(..., description=TITLE_DESC, example="Do the dishes")


class OptionalTitleField(BaseModel):
    title: str | None = Field(None, description=TITLE_DESC, example="Do the dishes")


class DescriptionField(BaseModel):
    description: str | None = Field(
        None, description=DESCRIPTION_DESC, example="Wash all dishes after dinner"
    )


class OptionalDescriptionField(BaseModel):
    description: str | None = Field(
        None, description=DESCRIPTION_DESC, example="Wash all dishes after dinner"
    )


class StatusField(BaseModel):
    status: TaskStatus = Field(
        TaskStatus.PENDING, description=STATUS_DESC, example="pending"
    )


class OptionalStatusField(BaseModel):
    status: TaskStatus | None = Field(None, description=STATUS_DESC, example="pending")


class AssignedToField(BaseModel):
    assigned_to: str | None = Field(
        None, description=ASSIGNED_TO_DESC, example="john.doe"
    )


class OptionalAssignedToField(BaseModel):
    assigned_to: str | None = Field(
        None, description=ASSIGNED_TO_DESC, example="john.doe"
    )


class DueDateField(BaseModel):
    due_date: date | None = Field(None, description=DUE_DATE_DESC, example="2025-09-30")


class OptionalDueDateField(BaseModel):
    due_date: date | None = Field(None, description=DUE_DATE_DESC, example="2025-09-30")


class CreatedAtField(BaseModel):
    created_at: datetime = Field(
        ..., description=CREATED_AT_DESC, example="2025-09-27T12:00:00"
    )


class UpdatedAtField(BaseModel):
    updated_at: datetime | None = Field(
        None, description=UPDATED_AT_DESC, example="2025-09-27T13:00:00"
    )


class OptionalStatusListField(BaseModel):
    status: list[TaskStatus] | None = Field(
        None, description=STATUS_DESC, example=["pending", "completed"]
    )


class TaskResponse(
    TaskConfig,
    IdField,
    TitleField,
    DescriptionField,
    StatusField,
    AssignedToField,
    DueDateField,
    CreatedAtField,
    UpdatedAtField,
):
    pass


class CreateTaskRequest(
    TaskConfig, TitleField, DescriptionField, StatusField, AssignedToField, DueDateField
):
    pass


class PatchTaskRequest(
    TaskConfig,
    OptionalTitleField,
    OptionalDescriptionField,
    OptionalStatusField,
    OptionalAssignedToField,
    OptionalDueDateField,
):
    pass


class TaskFilterRequest(
    TaskConfig,
    OptionalTitleField,
    OptionalDescriptionField,
    OptionalAssignedToField,
    OptionalStatusListField,
):
    due_date_init_date: date | None = Field(
        None, description=INITIAL_DUE_DATE_DESC, example="2025-09-01"
    )
    due_date_end_date: date | None = Field(
        None, description=END_DUE_DATE_DESC, example="2025-09-30"
    )
    created_at_init_date: date | None = Field(
        None, description=INITIAL_CREATION_DATE_DESC, example="2025-09-01"
    )
    created_at_end_date: date | None = Field(
        None, description=END_CREATION_DATE_DESC, example="2025-09-30"
    )


class TaskReportRequest(TaskConfig, OptionalAssignedToField, OptionalStatusListField):
    init_date: date = Field(
        ..., description=REPORT_INIT_DATE_DESC, example="2025-09-01"
    )
    end_date: date = Field(..., description=REPORT_END_DATE_DESC, example="2025-09-30")


class AsyncTaskResponse(TaskConfig):
    task_id: str = Field(
        ...,
        description=CELERY_TASK_ID_DESC,
        example="c3b1a2d4-1234-5678-9abc-def012345678",
    )
