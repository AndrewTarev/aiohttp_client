import asyncio

from sqlalchemy import Column, Integer, String

from src.core.models.base import Base
from src.core.db_helper import db_helper


class Ticker(Base):
    __tablename__ = "tickers"

    id = Column(Integer, primary_key=True)
    currency = Column(String, index=True, nullable=False)
    price = Column(String, nullable=False)
    timestamp = Column(Integer, nullable=False)


async def create_tables():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await db_helper.engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_tables())
