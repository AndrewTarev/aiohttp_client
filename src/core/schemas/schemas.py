from pydantic import BaseModel, ConfigDict


class TickerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    ticker: str
    price: str
    timestamp: int
