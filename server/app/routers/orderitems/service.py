from fastapi import Depends, HTTPException
from sqlmodel import select, Session
from database.core import SessionDep
from models.model import OrderItem



async def get_number_of_order_items(session: SessionDep):
    result = await get_order_items(session)
    return {"number of order items": str(len(result))}


async def get_order_item(order_item_id: int, session: Session = Depends(SessionDep)):
    order_item = await session.query(OrderItem).filter(OrderItem.order_item_id == order_item_id).first()
    if not order_item:
        raise HTTPException(status_code=404, detail="order item not found")
    return order_item


async def get_order_items(session: SessionDep):
    result = await session.execute(select(OrderItem))
    return result.scalars().all()
