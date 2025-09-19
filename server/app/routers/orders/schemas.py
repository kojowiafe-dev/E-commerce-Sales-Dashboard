from sqlmodel import SQLModel
from datetime import datetime
from typing import List
from ..orderitems.schemas import OrderItemCreate, OrderItemResponse

class OrderBase(SQLModel):
    order_date: str
    purchase_address: str
    
    class Config:
        orm_mode = True

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]   # create order with items
    
    class Config:
        orm_mode = True

class OrderResponse(OrderBase):
    order_id: int
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True
        