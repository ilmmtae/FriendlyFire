from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio.session import AsyncSession

from src.db.operations.account import AccountManager
from src.schema.account import  CreateAccountRequest, AccountResponse


class AccountService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.manager = AccountManager(db)

    async def create_account(self, request: CreateAccountRequest) -> AccountResponse:
        if await self.manager.email_taken(email=request.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already taken")

        account = await self.manager.create_account(request=request)
        return AccountResponse(**account.__dict__)

    async def list_accounts(self) -> list[AccountResponse]:
        accounts = await self.manager.list_accounts()
        return [AccountResponse(**account.__dict__) for account in accounts]

