from sqlmodel import SQLModel
from typing import List, Optional

class ProductBase(SQLModel):
    name: str
    price_each: float
    
    class Config:
        orm_mode = True

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    product_id: int

    class Config:
        orm_mode = True
        
        
class PaginatedProducts(SQLModel):
    items: List[ProductResponse]
    total: int