from fastapi import APIRouter, Depends, HTTPException, status
from routers.products import schemas, service
from database.core import SessionDep
from typing import List



router = APIRouter(
    prefix="/products", 
    tags=["Products"]
)


@router.get("/total_products")
async def get_number_of_products(session: SessionDep):
    result = await service.get_number_of_products(session)
    return result

@router.get("/{product_id}", response_model=schemas.ProductResponse)
async def get_product(product_id: int, session: SessionDep):
    product = await service.get_product(product_id, session)
    return product

@router.get("/", response_model=List[schemas.ProductResponse])
async def get_products(session: SessionDep):
    products = await service.get_products(session)
    return products