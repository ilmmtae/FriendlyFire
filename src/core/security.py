from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from pwdlib import PasswordHash
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.config import settings
from src.dependencies.database import RWSessionStub


SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

password_hash = PasswordHash.recommended()
security_scheme = HTTPBearer()


async def get_token(
    auth: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = auth.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        account_id = payload.get("sub")
        if account_id is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired")
    except jwt.InvalidTokenError:
        raise credentials_exception
    return account_id



async def get_current_user(
    auth: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: AsyncSession = Depends(RWSessionStub)
):
    from src.service.account import AccountService

    token = auth.credentials

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        account_id = payload.get("sub")

        if not account_id:
            raise HTTPException(status_code=401)

        account = await AccountService(db=db).get_account_by_id(account_id)
        if not account:
            raise HTTPException(status_code=401)

        return account
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")