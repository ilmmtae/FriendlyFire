from fastapi import Request, HTTPException, status
from src.core.redis import redis_client

class RateLimiter:
    def __init__(self, times: int, seconds: int):
        self.times = times
        self.seconds = seconds

    async def __call__(self, request: Request):
        ip = request.client.host
        key = f"rate_limit:{ip}:{request.url.path}"

        res = await redis_client.incr(key)

        if res == 1:
            await redis_client.expire(key, self.seconds)

        if res > self.times:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Try again later."
            )


