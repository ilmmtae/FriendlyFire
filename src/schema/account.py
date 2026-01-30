from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AgeResponse(BaseModel):
    age: int = Field(..., description="The calculated age")

class CreateAccountRequest(BaseModel):
      first_name: str = Field(..., description="The first name of the account holder")
      last_name: str = Field(..., description="The last name of the account holder")
      email: str = Field(..., description="The email of the account holder")
      image: str | None = Field(None, description="The image URL of the account holder")

class AccountResponse(BaseModel):
        id: UUID = Field(..., description="The unique identifier of the account")
        first_name: str = Field(..., description="The first name of the account holder")
        last_name: str = Field(..., description="The last name of the account holder")
        email: str = Field(..., description="The email of the account holder")
        image: str | None = Field(None, description="The image URL of the account holder")
        is_deleted: bool = Field(..., description="Indicates if the account is deleted")
        created_at: datetime = Field(..., description="The creation timestamp of the account")
        updated_at: datetime = Field(..., description="The last update timestamp of the account")
        type: str = Field(..., description="Type of the account")

