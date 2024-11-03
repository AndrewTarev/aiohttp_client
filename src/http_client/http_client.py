import asyncio
import ssl

import aiohttp

from src.http_client.orm_operation import save_ticker_to_db


class DeribitClient:
    """
    Класс для взаимодействия с API Deribit для получения цен индексов.

    Использует асинхронные методы для запроса данных и хранения цен в базе данных.
    """

    api_url = "https://deribit.com/api/v2/public/get_index_price"

    async def fetch_index_price(self, session, currency) -> str:
        """
        Получает индексную цену для указанной валюты.

        :param session: Асинхронная сессия HTTP (aiohttp.ClientSession), используемая для выполнения запроса.
        :param currency: Строка, представляющая валюту для запроса, например, "btc_usd" или "eth_usd".
        :return: Индексная цена в виде строки.
        :raises Exception: В случае ошибки при выполнении запроса или отсутствия данных в ответе.

        Пример использования:

        async with aiohttp.ClientSession() as session:
            price = await client.fetch_index_price(session, "btc_usd")

        """
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        async with session.get(
            self.api_url,
            params={"index_name": currency},
            ssl=ssl_context,
        ) as response:
            data = await response.json()
            return str(data["result"]["index_price"])

    async def fetch_and_store_prices(self):
        """
        Бесконечный цикл для регулярного получения цен BTC и ETH и их хранения в базе данных.

        Запрашивает индексные цены для "btc_usd" и "eth_usd" каждые 60 секунд.
        Использует метод `fetch_index_price` для получения данных и
        функция `save_ticker_to_db` для их сохранения.

        Этот метод должен быть запущен в контексте асинхронного цикла событий.

        Пример использования:

        await client.fetch_and_store_prices()

        """

        async with aiohttp.ClientSession() as session:
            while True:
                btc_price = await self.fetch_index_price(session, "btc_usd")
                eth_price = await self.fetch_index_price(session, "eth_usd")
                await save_ticker_to_db("btc_usd", btc_price)
                await save_ticker_to_db("eth_usd", eth_price)
                await asyncio.sleep(60)


client = DeribitClient()

if __name__ == "__main__":
    asyncio.run(client.fetch_and_store_prices())
