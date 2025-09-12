from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, Session
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from schemas import ProductCreate, ProductResponse
from database import SessionDep
from typing import List
from models.model import Product

router = APIRouter(
    prefix="/products", 
    tags=["Products"]
)

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(SessionDep)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

@router.get("/", response_model=List[ProductResponse])
async def read_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(SessionDep)):
    products = await db.exec(select(Product).offset(skip).limit(limit)).all()
    return products