from datetime import datetime, timedelta, timezone
from typing import Union, Annotated, Optional

import jwt
from fastapi import Depends, HTTPException, status
from pwdlib import PasswordHash
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.config.config import settings

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

password_hash = PasswordHash.recommended()
security_scheme = HTTPBearer()


def create_access_token(account_id: str, expires_minutes: int | None = 15):
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode = {"sub": account_id, "exp": expire.timestamp()}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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
