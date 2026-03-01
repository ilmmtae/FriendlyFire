from typing import Any
from uuid import UUID

from src.db.base import async_session

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select, delete, update

from src.db.models.account import Account
from src.schema.account import CreateAccountRequest, ShortAccountSchema
from src.schema.authentication import LoginRequest


class AccountManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_account(self, request: CreateAccountRequest):
        account: Account = Account(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            image=request.image,
            password=request.password
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

    async def get_by_id(self, account_id: UUID) -> Any | None:
        result = await self.db.execute(select(Account).where(Account.id == account_id))
        return result.scalars().one_or_none()

    async def delete_by_id(self, account_id: UUID) -> None:
        await self.db.execute(delete(Account).where(Account.id == account_id))
        await self.db.commit()

    async def update_by_id(self, account_id: UUID, request: ShortAccountSchema) -> Account:
        await self.db.execute(update(Account).where(Account.id == account_id).values(**request.model_dump(exclude_unset=True)))
        await self.db.commit()
        result = await self.db.execute(select(Account).where(Account.id == account_id))
        return result.scalars().one()

    async def get_by_email(self, email: str) -> Account | None:
        result = await self.db.execute(select(Account).where(Account.email == email))
        return result.scalars().one_or_none()

    async def update_account_verification(self, account_id: UUID, phone: str) -> None:
        stmt = (
            update(Account)
            .where(Account.id == account_id)
            .values(phone_number=phone, is_phone_verified=True)
        )
        await self.db.execute(stmt)
        await self.db.commit()