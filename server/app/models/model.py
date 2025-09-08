from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from uuid import uuid4, UUID
from pydantic import EmailStr
from sqlalchemy import Column, Enum as SqlEnum
from datetime import date, datetime
from typing import Optional, List

class RoleEnum(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"
    
    

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False)
    role: RoleEnum = Field(
        sa_column=Column(SqlEnum(RoleEnum, name="roleenum"), nullable=False),
        default=RoleEnum.VIEWER,
    )
    
    
    
class Product(SQLModel, table=True):
    __tablename__ = "products"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price_each: float
    
    
    
class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: int | None = Field(default=None, primary_key=True)
    order_date: str = Field(default=None)
    purchase_address: str = Field(default=None)
    
    # Relationship
    items: List["OrderItem"] = Relationship(back_populates="order")

    
    
    
class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", nullable=False)
    product_id: int = Field(foreign_key="products.id", nullable=False)
    quantity: int = Field(default=1, nullable=False)
    price_each: float = Field(default=0.0, nullable=False)
    line_total: float = Field(default=0.0, nullable=False)
