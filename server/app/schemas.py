from sqlmodel import SQLModel, Field
from datetime import datetime, date
from typing import Optional, List
from uuid import uuid4
from pydantic import EmailStr
from models.model import RoleEnum

    
    
class UserBase(SQLModel):
    name: str
    email: Optional[str] = None
    phone: str
    house_address: str
    role: RoleEnum

class UserRegister(UserBase):
    password: str

class UserLogin(SQLModel):
    name: str
    password: str
    role: str
    
    
    
class ProductBase(SQLModel):
    id: uuid4
    name: str
    price: float
    category: str
    inventory_count: str
    
    

class OrderBase(SQLModel):
    id: uuid4
    order_date: date
    total_amount: float
    
    
class OrderItemBase(SQLModel):
    id: uuid4
    order_id: uuid4
    product_id: uuid4
    quantity: int
    price_each: float
    line_total: float