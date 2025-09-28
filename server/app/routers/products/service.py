from fastapi import Depends, HTTPException, status
from sqlmodel import func, select, Session
from database.core import SessionDep
from models.model import OrderItem, Product
from routers.products import schemas



async def get_top_products(session: SessionDep, limit: int = 5):
    query = (
        select(Product.name, func.sum(OrderItem.quantity).label("total_sold"))
        .join(OrderItem.product)
        .group_by(Product.name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(limit)
    )
    result = await session.execute(query)
    return [{"name": row[0], "total_sold": row[1]} for row in result]
    


async def get_number_of_products(session: SessionDep):
    result = await session.execute(select(func.count(Product.product_id)))
    result = result.scalars().first()
    return {"number of products": str(result)}



async def get_product(product_id: int, session: SessionDep):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


async def get_products(session: SessionDep, page: int = 1, limit: int = 10, search: str = None):
    offset = (page - 1) * limit

    query = select(Product)

    if search:
        query = query.where(Product.name.ilike(f"%{search}%"))

    products = await session.execute(
        query.order_by(Product.product_id).offset(offset).limit(limit)
    )
    products = products.scalars().all()

    # count total for pagination
    count_query = select(func.count(Product.product_id))
    if search:
        count_query = count_query.where(Product.name.ilike(f"%{search}%"))

    total = await session.execute(count_query)
    total = total.scalars().first()

    return schemas.PaginatedProducts(
        items=[schemas.ProductResponse.from_orm(p) for p in products],
        total=int(total),
    )









async def get_product_name(name: str, session: SessionDep):
    # product = await session.get(Product, name)
    product = await session.execute(select(Product).where(Product.name == name))
    product = product.scalars().first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product
