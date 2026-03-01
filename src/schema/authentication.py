from uuid import UUID

from pydantic import BaseModel



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
    refresh_token: str


class TokenData(BaseModel):
    account_id: str | UUID = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class DeeplinkResponse(BaseModel):
    deeplink: str

class VerifyDeeplinkRequest(BaseModel):
    token: str
    phone: str