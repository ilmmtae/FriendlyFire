from typing import List

from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends, status, APIRouter

from src.dependencies.database import RWSessionStub
from src.schema.account import CreateAccountRequest, AccountResponse
from src.service.account import AccountService

account_router = APIRouter(prefix="/account", tags=["account"])


@account_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create an account",
    description="This endpoint creates a new account with the provided details.",
    response_model=AccountResponse,
)
async def create_account(
    request: CreateAccountRequest, db: AsyncSession = Depends(RWSessionStub)
) -> AccountResponse:
    return await AccountService(db=db).create_account(request)


@account_router.get("")
async def list_accounts(
    db: AsyncSession = Depends(RWSessionStub),
) -> List[AccountResponse]:
    return await AccountService(db=db).list_accounts()
