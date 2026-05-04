from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import get_token
from src.dependencies.database import RWSessionStub
from src.schema.account import AccountResponse
from src.service.account import AccountService
from src.core.security import oauth2_scheme

me_router = APIRouter(prefix="/me", tags=["Me"])


@me_router.get("")
async def get_my_account(
    token: str = Depends(get_token),
    db: AsyncSession = Depends(RWSessionStub),
) -> AccountResponse:
    return await AccountService(db).get_account_by_id(account_id=token)

@me_router.get("/me")
async def get_my_profile(token: str = Depends(oauth2_scheme)):
    return {"token": token}
