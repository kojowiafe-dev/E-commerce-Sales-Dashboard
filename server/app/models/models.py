from sqlmodel import SQLModel, Field
from enum import Enum
from uuid import uuid4
from pydantic import EmailStr
from datetime import date

class RoleEnum(str, Enum):
    admin = "admin"
    analyst = "analyst"
    admin = "admin"
    
    

class User(SQLModel, table=True):
    id: uuid4 = Field(default=None, primary_key=True, index=True)
    name: str = Field()
    email: EmailStr
    role: RoleEnum
    password: str
    
    
    
class Product(SQLModel):
    id: uuid4
    name: str
    price: float
    category: str
    inventory_count: str
    
    

class Order(SQLModel):
    id: uuid4
    order_date: date
    total_amount: float
    
    
class OrderItem(SQLModel):
    id: uuid4
    order_id: uuid4
    product_id: uuid4
    quantity: int
    price_each: float
    line_total: float