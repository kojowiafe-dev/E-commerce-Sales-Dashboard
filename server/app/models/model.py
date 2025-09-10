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
    user_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False)
    role: RoleEnum = Field(
        sa_column=Column(SqlEnum(RoleEnum, name="roleenum"), nullable=False),
        default=RoleEnum.VIEWER,
    )
    
    
    def __repr__(self):
        return f"User(id={self.user_id}, name={self.name}, email={self.email})"
    
    
    
class Product(SQLModel, table=True):
    __tablename__ = "products"
    product_id: int = Field(default=None, primary_key=True, index=True)
    name: str = Field(nullable=False, index=True)
    price_each: float = Field(nullable=False)
    
    # Relationship
    order_items: List["OrderItem"] = Relationship(back_populates="product")


    def __repr__(self):
        return f"Product(id={self.product_id}, name={self.name}, price={self.price_each})"
    
    
    
class Order(SQLModel, table=True):
    __tablename__ = "orders"

    order_id: int | None = Field(default=None, primary_key=True)
    order_date: str = Field(default=None)
    purchase_address: str = Field(default=None)
    
    # Relationship
    items: List["OrderItem"] = Relationship(back_populates="order")
    
    
    def __repr__(self):
        return f"Order(id={self.order_id}, date={self.order_date}, purchase={self.purchase_address})"
    
    
    
class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    order_item_id: int = Field(default=None, primary_key=True, index=True)
    order_id: int = Field(foreign_key="orders.order_id", nullable=False)
    product_id: int = Field(foreign_key="products.product_id", nullable=False)
    quantity: int = Field(default=1, nullable=False)
    price_each: float = Field(default=0.0, nullable=False)
    line_total: float = Field(default=0.0, nullable=False)
    
    
    # Relationship
    order: List["Order"] = Relationship(back_populates="items")
    product: List["Product"] = Relationship(back_populates="order_items")
    
    
    def __repr__(self):
        return f"OrderItem(order={self.order_id}, product={self.product_id}, qty={self.quantity}, total={self.line_total})"