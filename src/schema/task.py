from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class ShortTaskSchema(BaseModel):
    task_title: str = Field(..., description="Task title")
    instructions: str | None = Field(None, description="Instructions")
    max_score: int = Field(100, description="Max score", ge=0, le=100)
    due_date: datetime | None = Field(None, description="Deadline")

class CreateTaskRequest(ShortTaskSchema):
    course_id: UUID = Field(..., description="Сourse ID to which we attach the task")

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v: datetime | None):
        if v:
            if v < datetime.now():
                raise ValueError("Deadline must be in the future")
        return v

    model_config = {
        "json_schema_extra":{
            "example": {
                "task_title": "Python",
                "instructions": "Learning python",
                "max_score": 100,
                "due_date": "2026-01-24T11:00:00",
                "course_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
            }
        }
    }

class TaskResponse(ShortTaskSchema):
    id: UUID = Field(...)
    course_id: UUID = Field(...)

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "course_id": "123e4567-e89b-12d3-a456-426614174000",
                "task_title": "Task №1",
                "max_score": 100
            }
        }
    }
