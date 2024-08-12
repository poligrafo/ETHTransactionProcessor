import logging
import aioredis
import json

from app.utils import decimal_default


logger = logging.getLogger(__name__)
redis = aioredis.from_url("redis://redis:6379/0", encoding="utf-8", decode_responses=True)


async def get_from_cache(key: str):
    data = await redis.get(key)
    if data:
        return json.loads(data)
    return None


async def set_to_cache(key: str, value: any, expire: int):
    try:
        serialized_value = json.dumps(value, default=decimal_default)
        await redis.set(key, serialized_value, ex=expire)
    except TypeError as e:
        logger.error(f"Serialization error: {e}")
        raise
