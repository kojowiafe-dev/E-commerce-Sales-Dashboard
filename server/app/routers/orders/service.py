from fastapi import Depends, HTTPException
from sqlmodel import select, Session
from database.core import SessionDep
from models.model import Order



async def get_number_of_orders(session: SessionDep):
    result = await get_orders(session)
    return {"number of orders": str(len(result))}


async def get_order(order_id: int, session: Session = Depends(SessionDep)):
    order = await session.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Product not found")
    return order


async def get_orders(session: SessionDep):
    result = await session.execute(select(Order))
    return result.scalars().all()
