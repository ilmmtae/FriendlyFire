from datetime import datetime
from uuid import UUID

from email_validator import validate_email, EmailNotValidError
from pydantic import BaseModel, Field, field_validator, EmailStr

from src.db.types.account import AccountType

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class ShortAccountSchema(BaseModel):
    first_name: str | None = Field(None, description="The first name of the account holder")
    last_name: str | None = Field(None, description="The last name of the account holder")
    image: str | None = Field(None, description="The image URL of the account holder")
    email: str = Field(..., pattern=EMAIL_REGEX, description="User email address")

class CreateAccountRequest(ShortAccountSchema):
    password: str = Field(..., description="The password of the account holder")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")

        special_chars = "@#$%^&+=_-"
        if not any(char in special_chars for char in v):
            raise ValueError("Password must contain at least one special character")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "test@gmail.com",
                "image": "http://example.com/image.jpg",
                "password": "Pass+word",
            }
        }
    }


class AccountResponse(ShortAccountSchema):
    id: UUID = Field(..., description="The unique identifier of the account")
    is_deleted: bool = Field(..., description="Indicates if the account is deleted")
    created_at: datetime = Field(
        ..., description="The creation timestamp of the account"
    )
    updated_at: datetime = Field(
        ..., description="The last update timestamp of the account"
    )
    type: str | None = Field(None, description="Type of the account")
    phone_number: str | None = None

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


class AccountRegisterResponse(BaseModel):
    account: AccountResponse
    access_token: str
    token_type: str = "bearer"

class UserInvite(BaseModel):
    email: EmailStr
