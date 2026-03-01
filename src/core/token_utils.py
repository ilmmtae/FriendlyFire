from datetime import datetime, timezone, timedelta
import jwt
from src.config.config import settings

def create_access_token(account_id: str, expires_minutes: int | None = 15):
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode = {"sub": account_id, "exp": expire.timestamp(), "type": "access"}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def create_refresh_token(account_id: str, expires_days: int | None = 5):
    expire = datetime.now(timezone.utc) + timedelta(days=expires_days)
    to_encode = {"sub": account_id, "exp": expire.timestamp(), "type": "refresh"}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)