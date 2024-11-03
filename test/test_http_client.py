import aiohttp
import pytest
from aioresponses import aioresponses

from src.http_client.http_client import DeribitClient


@pytest.mark.asyncio
async def test_fetch_index_price():
    client = DeribitClient()
    currency = "btc_usd"
    expected_price = "12345.67"

    mock_response = {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {"index_price": expected_price},
    }

    with aioresponses() as m:
        m.get(
            f"https://deribit.com/api/v2/public/get_index_price?index_name={currency}",
            payload=mock_response,
        )

        async with aiohttp.ClientSession() as session:
            price = await client.fetch_index_price(session, currency)

    assert price == expected_price


@pytest.mark.asyncio
async def test_fetch_index_price_no_result():
    client = DeribitClient()
    currency = "btc_usd"

    mock_response = {"jsonrpc": "2.0", "id": 1, "result": {}}

    with aioresponses() as m:
        m.get(
            f"https://deribit.com/api/v2/public/get_index_price?index_name={currency}",
            payload=mock_response,
        )

        async with aiohttp.ClientSession() as session:
            with pytest.raises(KeyError):  # Мы ожидаем, что будет исключение KeyError
                await client.fetch_index_price(session, currency)
