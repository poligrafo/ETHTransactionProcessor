import pytest
from unittest.mock import patch
from app.core.celery.tasks import fetch_and_save_latest_transactions


@pytest.mark.asyncio
async def test_celery_task(monkeypatch):
    mock_result = "mocked_result"

    with patch("app.core.celery.tasks.fetch_and_save_latest_transactions.apply_async") as mock_task:
        mock_task.return_value.get.return_value = mock_result
        tx_hash = "2f4228659dee1416b88e984be9b8a19fad8fa6ee8c9f7cdc0c80c7869da8bf8a"
        task = fetch_and_save_latest_transactions.apply_async(args=[tx_hash])
        result = task.get(timeout=30)
        assert result == mock_result
