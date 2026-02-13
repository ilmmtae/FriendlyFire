from uuid import UUID

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select

from sqlalchemy.ext.asyncio.session import AsyncSession

from src.core.security import password_hash, create_access_token
from src.db.models.account import Account
from src.db.operations.account import AccountManager
from src.schema.account import CreateAccountRequest, AccountResponse, ShortAccountSchema
from src.schema.authentication import LoginRequest, TokenResponse


class AccountService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.account_manager = AccountManager(db)

    async def create_account(self, request: CreateAccountRequest) -> AccountResponse:
        if await self.account_manager.email_taken(email=request.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already taken"
            )

        request.password = password_hash.hash(request.password)

        account = await self.account_manager.create_account(request=request)
        return AccountResponse(**account.__dict__)

    async def list_accounts(self) -> list[AccountResponse]:
        accounts = await self.account_manager.list_accounts()
        return [AccountResponse(**account.__dict__) for account in accounts]

    async def _get_account_or_404(self, account_id: UUID) -> Account:
        account = await self.account_manager.get_by_id(account_id=account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
            )
        return account

    async def get_account_by_id(self, account_id: UUID) -> AccountResponse:
        account = await self._get_account_or_404(account_id=account_id)
        return AccountResponse(**account.__dict__)

    async def delete_account_by_id(self, account_id: UUID) -> None:
        await self.account_manager.delete_by_id(account_id=account_id)

    async def update_account_by_id(
        self, account_id: UUID, request: ShortAccountSchema
    ) -> AccountResponse:

        await self._get_account_or_404(account_id=account_id)

        account = await self.account_manager.update_by_id(
            account_id=account_id, request=request
        )
        return AccountResponse(**account.__dict__)

    async def authenticate(self, request: LoginRequest) -> TokenResponse:
        account = await self.account_manager.get_by_email(email=request.email)

        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
            )
        if not password_hash.verify(request.password, account.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
            )

        access_token = create_access_token(account_id=str(account.id))
        return TokenResponse(access_token=access_token, token_type="bearer")
