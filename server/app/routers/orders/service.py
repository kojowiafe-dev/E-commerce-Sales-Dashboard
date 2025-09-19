from fastapi import Depends, HTTPException, status
from sqlmodel import select, Session
from database.core import SessionDep
from models.model import Order
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select


async def get_number_of_orders(session: SessionDep):
    result = await get_orders(session)
    return {"number of orders": str(len(result))}


from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.core import get_session


async def get_order(order_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(
        select(Order).options(selectinload(Order.items)).where(Order.id == order_id)
    )
    order = result.one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order



async def get_order(order_id: int, session: SessionDep):
    order = await session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    return order




# async def get_order(order_id: int, session: SessionDep):
#     result = await session.execute(
#         select(Order).options(selectinload(Order.items)).where(Order.order_id == order_id)
#     )
#     order = result.scalars().first()
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return order



async def get_orders(session: SessionDep):
    result = await session.execute(select(Order))
    return result.scalars().all()
