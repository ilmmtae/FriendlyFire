from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.db.types.account import AccountType

class ShortAccountSchema(BaseModel):
    first_name: str | None = Field(None, description="The first name of the account holder")
    last_name: str | None = Field(None, description="The last name of the account holder")
    image: str | None = Field(None, description="The image URL of the account holder")

class CreateAccountRequest(ShortAccountSchema):
    email: str = Field(..., description="The email of the account holder")
    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "test@gmail.com",
                "image": "http://example.com/image.jpg",
            }
        }
    }

class AccountResponse(ShortAccountSchema):
    id: UUID = Field(..., description="The unique identifier of the account")
    email: str = Field(..., description="The email of the account holder")
    is_deleted: bool = Field(..., description="Indicates if the account is deleted")
    created_at: datetime = Field(
        ..., description="The creation timestamp of the account"
    )
    updated_at: datetime = Field(
        ..., description="The last update timestamp of the account"
    )
    type: str | None = Field(None, description="Type of the account")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "first_name": "John",
                "last_name": "Doe",
                "email": "test@gmail.com",
                "image": "http://example.com/image.jpg",
                "is_deleted": False,
                "created_at": "2023-10-01T12:00:00",
                "updated_at": "2023-10-01T12:00:00",
                "type": AccountType.STUDENT,
            }
        }
    }
