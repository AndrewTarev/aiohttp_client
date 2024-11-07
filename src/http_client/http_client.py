from src.core.db_helper import db_helper
from src.core.logging_config import my_logger
from src.http_client.orm_operation import save_ticker_to_db

import aiohttp
import asyncio
import ssl


class DeribitClient:
    """
    Класс для взаимодействия с API Deribit для получения цен индексов.

    Использует асинхронные методы для запроса данных и хранения цен в базе данных.
    """

    API_URL = "https://deribit.com/api/v2/public/get_index_price"
    TIMEOUT = 10  # Максимальное время ожидания ответа

    async def fetch_index_price(
        self, session: aiohttp.ClientSession, currency: str
    ) -> str:
        """
        Получает индексную цену для указанной валюты.

        :param session: Асинхронная сессия HTTP (aiohttp.ClientSession), используемая для выполнения запроса.
        :param currency: Строка, представляющая валюту для запроса, например, "btc_usd" или "eth_usd".
        :return: Индексная цена в виде строки.
        :raises ValueError: В случае некорректного ответа API.

        Пример использования:
            async with aiohttp.ClientSession() as session:
                price = await client.fetch_index_price(session, "btc_usd")
        """
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        try:
            params = {"index_name": currency}
            async with session.get(
                self.API_URL,
                params=params,
                ssl=ssl_context,
                timeout=self.TIMEOUT,
            ) as response:

                response.raise_for_status()  # Генерирует исключение для ошибок статуса
                data = await response.json()
                print(data)
                # Проверка корректности полученного ответа
                if "result" not in data or "index_price" not in data["result"]:
                    raise ValueError(f"Некорректный ответ API: {data}")

                return str(data["result"]["index_price"])

        except aiohttp.ClientError as e:
            my_logger.info(f"Ошибка при выполнении запроса к API: {e}")
        except asyncio.TimeoutError:
            my_logger.info("Таймаут при ожидании ответа от API")
        except Exception as e:
            my_logger.info(f"Произошла ошибка: {e}")

    async def fetch_and_store_prices(self) -> None:
        """
        Бесконечный цикл для регулярного получения цен BTC и ETH и их хранения в базе данных.

        Запрашивает индексные цены для "btc_usd" и "eth_usd" каждые 60 секунд.
        Использует метод fetch_index_price для получения данных и
        функцию save_ticker_to_db для их сохранения.

        Этот метод должен быть запущен в контексте асинхронного цикла событий.

        Пример использования:
            await client.fetch_and_store_prices()
        """
        async with aiohttp.ClientSession() as session:
            while True:
                btc_price = await self.fetch_index_price(session, "btc_usd")
                eth_price = await self.fetch_index_price(session, "eth_usd")

                async with db_helper.session_factory() as db_session:
                    await save_ticker_to_db(
                        db_session=db_session, currency="btc_usd", price=btc_price
                    )
                    await save_ticker_to_db(
                        db_session=db_session, currency="eth_usd", price=eth_price
                    )

                await asyncio.sleep(60)  # Ожидание перед следующим запросом


client = DeribitClient()

if __name__ == "__main__":
    asyncio.run(client.fetch_and_store_prices())
