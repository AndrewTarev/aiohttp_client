from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.models import Ticker


class OrmOperation:
    """
    Класс OrmOperation предоставляет статические методы для работы с объектами Ticker в базе данных.
    Методы выполняют операции получения тикеров на основе различных критериев.
    """

    @staticmethod
    async def get_ticker_from_db(session: AsyncSession, ticker: str) -> list[Ticker]:
        """
        Получает список тикеров из базы данных по заданной валюте.

        :param session: Сессия базы данных типа AsyncSession.
        :param ticker: Строка, представляющая валюту тикера (например, "btc_usd", "eth_usd").
        :return: Список объектов Ticker, соответствующих заданной валюте.
        :raises HTTPException: Если тикер не найден, возвращает 404.

        Пример использования:

        tickers = await OrmOperation.get_ticker_from_db(session, "btc_usd")

        """
        query = select(Ticker).where(Ticker.ticker == ticker)
        results = await session.execute(query)
        ticker_instance = results.scalars().all()
        if not results:
            raise HTTPException(status_code=404, detail="Ticker not found")
        return list(ticker_instance)

    @staticmethod
    async def get_last_ticker(session: AsyncSession, ticker: str) -> Ticker:
        """
        Получает последний тикер из базы данных по заданной валюте.

        :param session: Сессия базы данных типа AsyncSession.
        :param ticker: Строка, представляющая валюту тикера (например, "btc_usd", "eth_usd").
        :return: Объект Ticker, представляющий последний тикер по заданной валюте.
        :raises HTTPException: Если тикер не найден, возвращает 404.

        Пример использования:

        last_ticker = await OrmOperation.get_last_ticker(session, "btc_usd")

        """
        query = (
            select(Ticker)
            .where(Ticker.ticker == ticker)
            .order_by(Ticker.timestamp.desc())
            .limit(1)
        )
        result = await session.execute(query)
        ticker_instance = result.scalars().first()
        if not ticker_instance:
            raise HTTPException(status_code=404, detail="Ticker not found")
        return ticker_instance

    @staticmethod
    async def get_filtered_tickers(
        session: AsyncSession,
        ticker: str,
        start_date: int,
        end_date: int,
    ) -> list[Ticker]:
        """
        Получает список тикеров из базы данных по заданной валюте и диапазону даты.

        :param session: Сессия базы данных типа AsyncSession.
        :param ticker: Строка, представляющая валюту тикера (например, "btc_usd", "eth_usd").
        :param start_date: Начальная дата (timestamp) для фильтрации тикеров.
        :param end_date: Конечная дата (timestamp) для фильтрации тикеров.
        :return: Список объектов Ticker, соответствующих заданной валюте и диапазону дат.
        :raises HTTPException: Если тикеры не найдены, возвращает 404.

        Пример использования:

        filtered_tickers = await OrmOperation.get_filtered_tickers(session, "btc_usd", 1633046400, 1635724800)

        """
        query = select(Ticker).where(
            Ticker.ticker == ticker,
            Ticker.timestamp >= start_date,
            Ticker.timestamp <= end_date,
        )
        results = await session.execute(query)
        ticker_instance = results.scalars().all()
        if not ticker_instance:
            raise HTTPException(status_code=404, detail="Prices not found")
        return list(ticker_instance)


orm = OrmOperation()
