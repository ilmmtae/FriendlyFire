from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class ShortCourseSchema(BaseModel):
    title: str = Field(..., description="Course title")
    description: str | None = Field(None, description="Course description")
    is_published: bool = Field(False, description="Has the course been published?")

class CreateCourseRequest(ShortCourseSchema):
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Studying Python",
                "description": "Python basics course",
                "is_published": True
            }
        }
    }

class CourseResponse(ShortCourseSchema):
    id: UUID = Field(..., description="Course ID")
    created_at: datetime | None = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Studying Python",
                "description": "Basics course",
                "is_published": True,
                "created_at": "2023-10-01T12:00:00"
            }
        }
    }

