from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

from src.db.models.account import Account
from src.schema.account import CreateAccountRequest


class AccountManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_account(self, request: CreateAccountRequest):
        account: Account = Account(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            image=request.image,
        )
        self.db.add(account)
        await self.db.commit()
        await self.db.refresh(account)
        return account

    async def list_accounts(self):
        result = await self.db.execute(select(Account))
        results = result.scalars().all()
        return results

    async def email_taken(self, email: str) -> bool:
        result = await self.db.execute(select(Account).where(Account.email == email))
        account = result.scalars().one_or_none()
        return account is not None
