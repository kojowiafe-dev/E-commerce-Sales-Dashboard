from fastapi import APIRouter, Depends, HTTPException, status
from routers.orders import schemas, service
from database.core import SessionDep
from typing import List



router = APIRouter(
    prefix="/order", 
    tags=["Orders"]
)


@router.get("/total-orders")
async def get_number_of_orders(session: SessionDep):
    result = await service.get_number_of_orders(session)
    return result

@router.get("/{order_id}", response_model=schemas.OrderResponse)
async def get_order(order_id: int, session: SessionDep):
    order = await service.get_order(order_id, session)
    return order

@router.get("/", response_model=List[schemas.OrderResponse])
async def get_orders(session: SessionDep):
    orders = await service.get_orders(session)
    return orders