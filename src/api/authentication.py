
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from authlib.integrations.starlette_client import OAuth

from src.api.redis import save_auth_token, get_user_id_by_token
from src.config.config import settings
from src.core.limiter import RateLimiter
from src.core.token_utils import create_access_token, create_refresh_token
from src.dependencies.database import RWSessionStub
from src.schema.authentication import RefreshTokenRequest, DeeplinkResponse, VerifyDeeplinkRequest
from src.schema.authentication import LoginRequest, TokenResponse
from src.service.account import AccountService
from src.core.security import get_current_user

authentication_router = APIRouter(prefix="/authentication", tags=["authentication"])



@authentication_router.post("/login", response_model=TokenResponse,
                            dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def login(request: LoginRequest, db: AsyncSession = Depends(RWSessionStub)) -> TokenResponse:
    return await AccountService(db=db).authenticate(request)


@authentication_router.post("/token", response_model=TokenResponse)
async def login_oauth_form(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(RWSessionStub)
):
    """Метод для Swagger UI (Authorize)"""
    return await AccountService(db=db).authenticate_oauth_user({
        "username": form_data.username,
        "password": form_data.password
    })


@authentication_router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(body: RefreshTokenRequest, db: AsyncSession = Depends(RWSessionStub)):
    try:
        payload = jwt.decode(body.refresh_token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        account_id = payload.get("sub")
        new_access = create_access_token(account_id=account_id)
        new_refresh = create_refresh_token(account_id=account_id)

        return TokenResponse(
            access_token=new_access,
            refresh_token=new_refresh,
            token_type="bearer"
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token expired or invalid")



@authentication_router.post("/set-password")
async def set_password(
        new_password: str,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(RWSessionStub)
):
    """Дозволяє користувачу, що зайшов через Google/GitHub, встановити пароль"""
    return await AccountService(db=db).set_initial_password(current_user.id, new_password)



oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

oauth.register(
    name='github',
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)



@authentication_router.get('/login/google')
async def login_google(request: Request):
    redirect_uri = request.url_for('auth_google')
    return await oauth.google.authorize_redirect(request, str(redirect_uri))


@authentication_router.get('/callback/google', name='auth_google')
async def auth_google(request: Request, db: AsyncSession = Depends(RWSessionStub)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    if user_info:
        return await AccountService(db=db).authenticate_oauth_user(user_info)
    raise HTTPException(status_code=400, detail="Google authentication failed")



@authentication_router.get('/login/github')
async def login_github(request: Request):
    redirect_uri = request.url_for('auth_github')
    return await oauth.github.authorize_redirect(request, str(redirect_uri))


@authentication_router.get('/auth/github', name='auth_github')
async def auth_github(request: Request, db: AsyncSession = Depends(RWSessionStub)):
    token = await oauth.github.authorize_access_token(request)
    resp = await oauth.github.get('user', token=token)
    user_info = resp.json()

    if not user_info.get('email'):
        emails_resp = await oauth.github.get('user/emails', token=token)
        user_info['email'] = next(e['email'] for e in emails_resp.json() if e['primary'])

    return await AccountService(db=db).authenticate_oauth_user(user_info)



@authentication_router.post("/generate-deeplink", response_model=DeeplinkResponse)
async def generate_deeplink(current_user=Depends(get_current_user)):
    if current_user.phone_number:
        raise HTTPException(status_code=400, detail="Account already verified")
    token = await save_auth_token(str(current_user.id))
    return {"deeplink": f"https://t.me/{settings.BOT_NAME}?start={token}"}


@authentication_router.post("/verify-deeplink")
async def verify_deeplink(request: VerifyDeeplinkRequest, db: AsyncSession = Depends(RWSessionStub)):
    user_uuid = await get_user_id_by_token(request.token)
    account = await AccountService(db=db).verify_phone(user_uuid, request.phone)
    access = create_access_token(account_id=str(account.id))
    refresh = create_refresh_token(account_id=str(account.id))
    return {"access_token": access, "refresh_token": refresh}