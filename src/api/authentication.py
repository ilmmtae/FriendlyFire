from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import RWSessionStub
from src.schema.authentication import LoginRequest, TokenResponse
from src.service.account import AccountService

authentication_router = APIRouter(prefix="/authentication", tags=["authentication"])


@authentication_router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest, db: AsyncSession = Depends(RWSessionStub)
) -> TokenResponse:
    return await AccountService(db=db).authenticate(request=request)
