from uuid import UUID

from pydantic import BaseModel

from src.schema.account import AccountResponse


class LoginRequest(BaseModel):
    email: str
    password: str
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "test@gmail.com",
                "password": "Pass+word",
            }
        }
    }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    account_id: str | UUID = None
