# routers/shared/schemas.py
from typing import Optional
from sqlmodel import SQLModel


class OrderBase(SQLModel):
    order_date: str
    purchase_address: str

    class Config:
        from_attributes = True


class OrderItemBase(SQLModel):
    quantity: int
    price_each: float
    line_total: float

    class Config:
        from_attributes = True
