from fastapi import Depends, HTTPException, status
from sqlmodel import select, Session
from database.core import SessionDep
from models.model import Order



async def get_number_of_orders(session: SessionDep):
    result = await get_orders(session)
    return {"number of orders": str(len(result))}


async def get_order(order_id: int, session: SessionDep):
    order = await session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return order


async def get_orders(session: SessionDep):
    result = await session.execute(select(Order))
    return result.scalars().all()
