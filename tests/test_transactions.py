from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.deps import get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_transaction():
    response = client.post(
        "/transactions/",
        json={"tx_hash": "0x123", "block_number": 1, "from_address": "0xabc", "to_address": "0xdef", "value": 10, "gas": 21000, "gas_price": 50},
    )
    assert response.status_code == 200
    assert response.json()["tx_hash"] == "0x123"


def test_read_transaction():
    response = client.get("/transactions/0x123")
    assert response.status_code == 200
    assert response.json()["tx_hash"] == "0x123"


def test_read_transactions():
    response = client.get("/transactions/")
    assert response.status_code == 200
    assert len(response.json()) > 0
