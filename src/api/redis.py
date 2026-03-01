import uuid

from src.core.redis import redis_client


async def save_auth_token(user_uuid: str, ttl: int = 3600) -> str:
    token = str(uuid.uuid4())
    await redis_client.setex(f"auth_session:{token}", ttl, user_uuid)
    return token


async def get_user_id_by_token(token: str) -> str | None:
    key = f"auth_session:{token}"
    user_uuid = await redis_client.get(key)

    if user_uuid:
        await redis_client.delete(key)

    return user_uuid