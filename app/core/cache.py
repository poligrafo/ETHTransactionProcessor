import logging
import aioredis
import json
from typing import Any

from app.utils import decimal_default

logger = logging.getLogger(__name__)


class CacheHandler:
    def __init__(self, redis_url: str = "redis://redis:6379/0"):
        self.redis = aioredis.from_url(redis_url, encoding="utf-8", decode_responses=True)

    async def get_from_cache(self, key: str) -> Any:
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    async def set_to_cache(self, key: str, value: Any, expire: int):
        try:
            serialized_value = json.dumps(value, default=decimal_default)
            await self.redis.set(key, serialized_value, ex=expire)
        except TypeError as e:
            logger.error(f"Serialization error: {e}")
            raise
