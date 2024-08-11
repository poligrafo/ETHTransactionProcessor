import aioredis
import json

redis = aioredis.from_url("redis://redis:6388/0", encoding="utf-8", decode_responses=True)


async def get_from_cache(key: str):
    data = await redis.get(key)
    if data:
        return json.loads(data)
    return None


async def set_to_cache(key: str, value, expire: int = 3600):
    await redis.set(key, json.dumps(value), ex=expire)
