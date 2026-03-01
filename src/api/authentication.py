from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.redis import save_auth_token, get_user_id_by_token
from src.config.config import settings
from src.core.limiter import RateLimiter
from src.core.redis import redis_client
from src.core.token_utils import create_access_token, create_refresh_token
from src.dependencies.database import RWSessionStub
from src.schema.authentication import RefreshTokenRequest, DeeplinkResponse, VerifyDeeplinkRequest
from src.schema.authentication import LoginRequest, TokenResponse
from src.service.account import AccountService
from src.core.security import get_current_user

authentication_router = APIRouter(prefix="/authentication", tags=["authentication"])


@authentication_router.post("/login", response_model=TokenResponse, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def login( request: LoginRequest, db: AsyncSession = Depends(RWSessionStub)) -> TokenResponse:
    return await AccountService(db=db).authenticate(request)



@authentication_router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(
    body: RefreshTokenRequest,
    db: AsyncSession = Depends(RWSessionStub)):
        try:
            payload = jwt.decode(body.refresh_token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
            if payload.get("type") != "refresh":
                raise HTTPException(status_code=401, detail="Invalid token type")

            account_id = payload.get("sub")
            new_access = create_access_token(account_id=account_id)
            new_refresh = create_refresh_token(account_id=account_id)

            account = await AccountService(db=db).get_account_by_id(account_id)
            if not account:
                raise HTTPException(status_code=401, detail="User not found")



            return TokenResponse(
                access_token=new_access,
                refresh_token=new_refresh,
                token_type="bearer"
            )
        except JWTError:
            raise HTTPException(status_code=401, detail="Refresh token expired or invalid")

@authentication_router.post("/generate-deeplink", response_model=DeeplinkResponse)
async def generate_deeplink(current_user = Depends(get_current_user)):
    if current_user.phone_number:
        raise HTTPException(status_code=400, detail="Account already verified")

    token = await save_auth_token(str(current_user.id))

    return {"deeplink": f"https://t.me/friendlyfireproject_bot?start={token}"}


@authentication_router.post("/verify-deeplink")
async def verify_deeplink(request: VerifyDeeplinkRequest, db: AsyncSession = Depends(RWSessionStub)):
    user_uuid = await get_user_id_by_token(request.token)
    account = await AccountService(db=db).verify_phone(user_uuid, request.phone)

    access = create_access_token(account_id=str(account.id))
    refresh = create_refresh_token(account_id=str(account.id))

    return {"access_token": access, "refresh_token": refresh}