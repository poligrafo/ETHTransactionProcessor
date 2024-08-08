import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_get_transactions():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/transactions")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_transaction():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        transaction_data = {
            "hash": "0x123",
            "from_address": "0xabc",
            "to_address": "0xdef",
            "value": 100,
            "gas": 21000,
            "gas_price": 50,
            "block_number": 123456
        }
        response = await ac.post("/api/v1/transactions", json=transaction_data)
    assert response.status_code == 200
    assert response.json()["hash"] == transaction_data["hash"]
