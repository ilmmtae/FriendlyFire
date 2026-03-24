import logging
import secrets
import time
from typing import List
from uuid import UUID
import httpx

from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import Depends, status, APIRouter, Path

from src.worker.tasks import send_invite_email_task
from src.config.config import settings
from src.core.limiter import RateLimiter
from src.core.security import get_token
from src.core.token_utils import create_access_token
from src.dependencies.database import RWSessionStub
from src.schema.account import (
    CreateAccountRequest,
    AccountResponse,
    ShortAccountSchema, AccountRegisterResponse, UserInvite, InviteSuccessResponse,
)
from src.schema.authentication import LoginRequest
from src.service.account import AccountService

DJANGO_WEBHOOK_URL = f"{settings.HOST}/webhook/user-sync/"
DJANGO_INVITE_URL = f"{settings.HOST}/api/internal/invite/"

logger = logging.getLogger(__name__)

async def sync_to_django(first_name: str, last_name: str, email: str, image: str, password: str = "default_pass"):
    async with httpx.AsyncClient() as client:
        try:
            payload = {
                "username": first_name,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
                "image_url": image
            }
            response = await client.post(DJANGO_WEBHOOK_URL, json=payload, timeout=5.0)
            response.raise_for_status()

            logger.info(
                f"Successfully synced account {email} with Django. "
                f"Status: {response.status_code}"
            )
        except httpx.HTTPStatusError as e:
            logger.error(f"Django sync failed with status {e.response.status_code}: {e.response.text}")
        except Exception as e:
            logger.error(f"Django synchronization unexpected error: {e}", exc_info=True)

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

    await sync_to_django(
        first_name=request.first_name or "New",
        last_name=request.last_name or "User",
        email=request.email,
        image=request.image or "",
        password=request.password
    )

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

@account_router.get("/link")
async def get_auth_link(
        db: AsyncSession = Depends(RWSessionStub),
        token: str = Depends(get_token),
):
    return AccountService(db=db)



@account_router.post(
    "/invite-to-social-network",
    status_code=status.HTTP_201_CREATED,
    response_model=InviteSuccessResponse
)
async def invite_to_social_network(
    request: CreateAccountRequest,
    db: AsyncSession = Depends(RWSessionStub)
) -> InviteSuccessResponse:
    start_time = time.time()

    service = AccountService(db=db)
    account = await service.create_account(request)
    invite_code = secrets.token_urlsafe(32)


    send_invite_email_task.delay(
        email=account.email,
        invite_code=invite_code,
        first_name=request.first_name or "User",
        last_name=request.last_name or ""
    )
    duration = time.time() - start_time

    logger.info(f"Invite task dispatched for {account.email} in {duration:.4f}s")

    return InviteSuccessResponse(
        status="success",
        account=account,
        invite_code=invite_code,
        dispatch_time=f"{duration:.4f}s"
    )