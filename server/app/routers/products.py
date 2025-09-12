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

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(SessionDep)):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/", response_model=List[ProductResponse])
async def get_products(session: SessionDep):
    result = await session.exec(select(Product)).all()
    return result