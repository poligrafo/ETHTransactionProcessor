import pytest
from unittest.mock import AsyncMock, patch
from app.core.cache import set_to_cache, get_from_cache


@pytest.mark.asyncio
@patch('app.core.cache.redis')
async def test_set_and_get_cache(mock_redis):
    mock_redis.set = AsyncMock()
    mock_redis.get = AsyncMock(return_value=None)

    cache_key = "test_transaction"
    transaction_data = {
        "hash": "0671661e0ccf9937179da2887f725fe4635c611de35d4490bd8d7e6fa4b6c6c8",
        "from_address": "0x653675b842d7d8b461f722b4117cb81dac8e639d",
        "to_address": "0xbb9bc244d798123fde783fcc1c72d3bb8c189413",
        "value": 1e18
    }

    await set_to_cache(cache_key, transaction_data, expire=60)
    result = await get_from_cache(cache_key)

    mock_redis.set.assert_called_once()
    mock_redis.get.assert_called_once()
    assert result is None

