from typing import List, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.orm.orm_operation import orm
from src.core.db_helper import db_helper

router = APIRouter(prefix="/api/v1", tags=["coin_info"])


@router.get("/prices")
async def get_prices(
    ticker: str,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Получает список всех тикеров для заданной валюты.

    ticker: Строка, представляющая валюту тикера (например, "btc_usd", "eth_usd").

    Пример запроса:

    GET /api/v1/prices?ticker=eth_usd

    """

    return await orm.get_ticker_from_db(
        session=session,
        ticker=ticker,
    )


@router.get("/prices/latest")
async def get_last_price(
    ticker: str,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Получает последний тикер для заданной валюты.

    ticker: Строка, представляющая валюту тикера (например, "btc_usd", "eth_usd").

    Пример запроса:

    GET /api/v1/prices/latest?ticker=eth_usd

    """

    return await orm.get_last_ticker(
        session=session,
        ticker=ticker,
    )


@router.get("/prices/filter")
async def get_prices_by_date(
    ticker: str,
    start_date: int,
    end_date: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Получает список тикеров для заданной валюты в указанном диапазоне дат.

    ticker: Строка, представляющая валюту тикера (например, "btc_usd", "eth_usd").

    start_date: Начальная дата в формате timestamp.

    end_date: Конечная дата в формате timestamp.

    Пример запроса:

    GET /api/v1/prices/filter?ticker=eth_usd&start_date=1633046400&end_date=1635724800

    """

    return await orm.get_filtered_tickers(
        session=session,
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
    )
