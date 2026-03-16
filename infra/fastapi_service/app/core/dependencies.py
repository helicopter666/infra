from collections.abc import AsyncGenerator
from typing import Annotated

import redis.asyncio as aioredis
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.redis_client import get_redis_pool
from app.core.config import settings
from app.core.security import decode_token
from app.db.session import async_session_factory

bearer_scheme = HTTPBearer()


# ── Database ──────────────────────────────────────────────────────────────────

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


# ── Redis ─────────────────────────────────────────────────────────────────────

async def get_redis() -> aioredis.Redis:
    return get_redis_pool()


# ── JWT / Current User ────────────────────────────────────────────────────────

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    redis: Annotated[aioredis.Redis, Depends(get_redis)],
) -> dict:
    token = credentials.credentials
    try:
        payload = decode_token(token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    jti = payload.get("jti", "")
    if await redis.exists(f"jwt:blacklist:{jti}"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")

    return payload


def require_role(*roles: str):
    """Factory: возвращает Depends, проверяющий роль пользователя."""
    def _check(current_user: Annotated[dict, Depends(get_current_user)]) -> dict:
        if current_user.get("role") not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user
    return Depends(_check)


# ── Типовые зависимости ───────────────────────────────────────────────────────

CurrentUser = Annotated[dict, Depends(get_current_user)]
AdminUser   = Annotated[dict, require_role("admin")]
DbSession   = Annotated[AsyncSession, Depends(get_db)]
Redis       = Annotated[aioredis.Redis, Depends(get_redis)]
