from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response
from src.config import settings

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.rate_limit_requests}/{settings.rate_limit_window}second"]
)

async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    response = Response(
        content=f"Rate limit exceeded: {exc.detail}",
        status_code=429
    )
    response.headers["Retry-After"] = str(exc.retry_after)
    return response
