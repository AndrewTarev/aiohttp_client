import time

from src.core.db_helper import db_helper
from src.core.models.models import Ticker


async def save_ticker_to_db(currency: str, price: str) -> None:
    """
    Сохраняет информацию о цене валюты в базе данных.

    Функция создает новую запись с указанием валюты, ее цены и временной метки и сохраняет её в базе данных.

    :param currency: Строка, представляющая код валюты (например, "btc_usd" или "eth_usd").
    :param price: Строка, представляющая цену валюты в виде строки (например, "50000.00").
    :return: None - функция не возвращает значения, используется для побочных эффектов в базе данных.
    :raises Exception: Может выбросить исключение в случае ошибки при добавлении записи в базу данных
          или при выполнении коммита транзакции.

    Пример использования:

    await save_ticker_to_db("btc_usd", "50000.00")
    """

    async with db_helper.session_factory() as db_session:
        timestamp = int(time.time())
        ticker: Ticker = Ticker(currency=currency, price=price, timestamp=timestamp)
        db_session.add(ticker)
        await db_session.commit()
