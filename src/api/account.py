from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends, status, APIRouter, Path

from src.core.limiter import RateLimiter
from src.core.security import create_access_token
from src.dependencies.database import RWSessionStub
from src.schema.account import (
    CreateAccountRequest,
    AccountResponse,
    ShortAccountSchema, AccountRegisterResponse,
)
from src.schema.authentication import LoginRequest
from src.service.account import AccountService

account_router = APIRouter(prefix="/account", tags=["account"])


@account_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create an account",
    description="This endpoint creates a new account with the provided details.",
    response_model=AccountRegisterResponse,
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
async def create_account(
    request: CreateAccountRequest, db: AsyncSession = Depends(RWSessionStub)
) -> AccountRegisterResponse:
    account: AccountResponse = await AccountService(db=db).create_account(request)
    access_token = create_access_token(account_id=str(account.id))

    return AccountRegisterResponse(
        account=account,
        access_token=access_token,
        token_type="bearer"
    )

@account_router.get("")
async def list_accounts(
    db: AsyncSession = Depends(RWSessionStub),
) -> List[AccountResponse]:
    return await AccountService(db=db).list_accounts()


@account_router.get("/{account_id}")
async def get_account_by_id(
    account_id: UUID = Path(..., description="The ID of the account to retrieve"),
    db: AsyncSession = Depends(RWSessionStub),
) -> AccountResponse:
    return await AccountService(db=db).get_account_by_id(account_id)


@account_router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account_by_id(
    account_id: UUID = Path(..., description="The ID of the account to delete"),
    db: AsyncSession = Depends(RWSessionStub),
) -> None:
    await AccountService(db=db).delete_account_by_id(account_id=account_id)


@account_router.patch("/{account_id}", status_code=status.HTTP_200_OK)
async def update_account_by_id(
    request: ShortAccountSchema,
    account_id: UUID = Path(..., description="The ID of the account to update"),
    db: AsyncSession = Depends(RWSessionStub),
) -> AccountResponse:
    return await AccountService(db=db).update_account_by_id(
        account_id=account_id, request=request
    )

