from datetime import datetime, timedelta, timezone
import jwt
from src.config.config import settings


def create_temp_token(user_uuid: str) -> str:
    payload = {
        "sub": str(user_uuid),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
    }

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    print(f"DEBUG: Сгенероване посилання: https://t.me/friendlyfireproject_bot?start={token}")

    return token