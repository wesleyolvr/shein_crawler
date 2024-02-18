from datetime import datetime

from pydantic import BaseModel


class PriceHistoryBase(BaseModel):
    date: datetime  # Use str para representar datas, pois Pydantic não aceita diretamente objetos datetime
    price: float


class PriceHistoryCreate(PriceHistoryBase):
    pass


class PriceHistoryRead(PriceHistoryBase):
    id: int

    class Config:
        orm_mode = True


class PriceHistoryUpdate(PriceHistoryBase):
    product_id: int
    new_price: float
