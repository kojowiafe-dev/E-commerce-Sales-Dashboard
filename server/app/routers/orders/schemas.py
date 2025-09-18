from sqlmodel import SQLModel
from datetime import datetime
from typing import List

class OrderBase(SQLModel):
    order_date: datetime
    purchase_address: str

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]   # create order with items

class OrderResponse(OrderBase):
    order_id: int
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True
        