from datetime import datetime, timedelta, timezone
from typing import Union, Annotated


import jwt
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError
from pwdlib import PasswordHash
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.config.config import settings

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

password_hash = PasswordHash.recommended()
security_scheme = HTTPBearer()

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_account_id(
    auth: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)]
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
    except InvalidTokenError:
        raise credentials_exception
    return account_id