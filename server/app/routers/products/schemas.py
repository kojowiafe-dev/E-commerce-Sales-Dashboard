from sqlmodel import SQLModel


class ProductBase(SQLModel):
    name: str
    price_each: float

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    product_id: int

    class Config:
        orm_mode = True