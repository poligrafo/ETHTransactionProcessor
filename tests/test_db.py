import pytest
from datetime import datetime
from unittest.mock import patch, AsyncMock
from app.models.transaction_models import Transaction

@pytest.mark.asyncio
@patch("app.db.session.SessionLocal", new_callable=AsyncMock)
async def test_save_transaction_to_db(mock_session):
    transaction_data = {
        "hash": "0671661e0ccf9937179da2887f725fe4635c611de35d4490bd8d7e6fa4b6c6c8",
        "from_address": "0x653675b842d7d8b461f722b4117cb81dac8e639d",
        "to_address": "0xbb9bc244d798123fde783fcc1c72d3bb8c189413",
        "value": int(1E+018),
        "gas": 21000,
        "gas_price": 21000000000,
        "fee": 441000000000000,
        "block_number": 1596977,
        "time": datetime.strptime("2016-05-28 00:00:12", "%Y-%m-%d %H:%M:%S"),
        "input_hex": "",
        "transaction_type": "call",
    }

    mock_db_session = mock_session.return_value.__aenter__.return_value

    new_transaction = Transaction(**transaction_data)
    mock_db_session.add(new_transaction)
    await mock_db_session.commit()

    mock_db_session.add.assert_called_once_with(new_transaction)
    mock_db_session.commit.assert_called_once()
