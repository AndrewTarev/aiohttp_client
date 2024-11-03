from pydantic import BaseModel


class TickerOut(BaseModel):
    id: int
    ticker: str
    price: str
    timestamp: int

    class Config:
        orm_mode = True
