import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.db.session import Base
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="module")
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="module")
def override_get_db(test_db):
    async def _override_get_db():
        yield test_db
    app.dependency_overrides[get_db] = _override_get_db


@pytest.mark.asyncio
async def test_create_transaction(async_client, override_get_db):
    response = await async_client.post(
        "/api/v1/transactions/",
        json={"tx_hash": "0x123", "block_number": 1, "from_address": "0xabc", "to_address": "0xdef", "value": 10, "gas_used": 21000, "gas_price_wei": 50},
    )
    assert response.status_code == 200
    assert response.json()["tx_hash"] == "0x123"


@pytest.mark.asyncio
async def test_read_transaction(async_client, override_get_db):
    response = await async_client.get("/api/v1/transactions/0x123")
    assert response.status_code == 200
    assert response.json()["tx_hash"] == "0x123"


@pytest.mark.asyncio
async def test_read_transactions(async_client, override_get_db):
    response = await async_client.get("/api/v1/transactions/")
    assert response.status_code == 200
    assert len(response.json()) > 0
