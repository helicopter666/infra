from datetime import timedelta

import redis.asyncio as aioredis

from app.core.config import settings

_pool: aioredis.Redis | None = None


def get_redis_pool() -> aioredis.Redis:
    global _pool
    if _pool is None:
        _pool = aioredis.from_url(
            str(settings.REDIS_URL),
            encoding="utf-8",
            decode_responses=True,
        )
    return _pool


async def close_redis_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.aclose()
        _pool = None


# ── Утилиты ───────────────────────────────────────────────────────────────────

async def cache_get(key: str) -> str | None:
    return await get_redis_pool().get(key)


async def cache_set(key: str, value: str, ttl: int | timedelta) -> None:
    r = get_redis_pool()
    if isinstance(ttl, timedelta):
        ttl = int(ttl.total_seconds())
    await r.setex(key, ttl, value)


async def cache_delete(key: str) -> None:
    await get_redis_pool().delete(key)


async def rate_limit_check(key: str, limit: int, window_seconds: int) -> bool:
    """
    Возвращает True если лимит не превышен, False если превышен.
    Использует атомарный INCR + EXPIRE.
    """
    r = get_redis_pool()
    current = await r.incr(key)
    if current == 1:
        await r.expire(key, window_seconds)
    return current <= limit
