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
async def test_fetch_index_price_http_error():
    client = DeribitClient()
    currency = "btc_usd"

    with aioresponses() as m:
        m.get(client.API_URL, status=500)

        async with aiohttp.ClientSession() as session:
            price = await client.fetch_index_price(session, currency)

        assert price is None  # Убедимся, что метод вернул None на ошибку
