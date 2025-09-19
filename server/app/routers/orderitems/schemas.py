from sqlmodel import SQLModel
from ..products.schemas import ProductResponse

class OrderItemBase(SQLModel):
    quantity: int
    price_each: float
    line_total: float
    
    class Config:
        orm_mode = True

class OrderItemCreate(OrderItemBase):
    product_id: int
    
    class Config:
        orm_mode = True

class OrderItemResponse(OrderItemBase):
    order_item_id: int
    product: ProductResponse   # nested product info

    class Config:
        orm_mode = True