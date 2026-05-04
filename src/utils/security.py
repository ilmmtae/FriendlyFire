from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext

from src.config.config import settings


def create_temp_token(user_uuid: str) -> str:
    payload = {
        "sub": str(user_uuid),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
    }

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)