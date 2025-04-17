"""
Shared Redis helper used by the service layer.
Install:  pip install redis[async]
Run:     docker run -p 6379:6379 -d redis
"""
import os, json, asyncio
from redis.asyncio import Redis
from datetime import timedelta

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DEFAULT_TTL = int(os.getenv("CACHE_TTL_SECONDS", "300"))  # 5 minutes

_redis: Redis | None = None


async def get_redis() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(REDIS_URL, decode_responses=True)
    return _redis


# ────────────────────────── helpers ──────────────────────────
async def cache_get(key: str):
    r = await get_redis()
    raw = await r.get(key)
    return json.loads(raw) if raw else None


async def cache_set(key: str, value, ttl: int | None = None):
    r = await get_redis()
    await r.set(key, json.dumps(value, default=str), ex=ttl or DEFAULT_TTL)


async def cache_delete_pattern(pattern: str):
    """
    Delete every Redis key that matches *pattern* (e.g. "users:*").
    """
    r = await get_redis()
    async for key in r.scan_iter(match=pattern):
        await r.delete(key)
