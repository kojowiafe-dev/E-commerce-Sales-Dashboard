from fastapi import Depends, HTTPException, status
from sqlmodel import select, Session
from database.core import SessionDep
from models.model import Product



async def get_number_of_products(session: SessionDep):
    result = await get_products(session)
    return {"number of products": str(len(result))}


# async def get_product(product_id: int, session: Session = Depends(SessionDep)):
#     product = await session.execute(Product).where(Product.product_id == product_id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return product


async def get_product(product_id: int, session: SessionDep):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


async def get_products(session: SessionDep):
    result = await session.execute(select(Product))
    return result.scalars().all()
