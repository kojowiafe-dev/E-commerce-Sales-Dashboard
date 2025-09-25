from fastapi import APIRouter, Depends, HTTPException, status
from routers.orderitems import schemas, service
from database.core import SessionDep
from typing import List



router = APIRouter(
    prefix="/order-items", 
    tags=["Order Items"]
)


@router.get("/total-order-items")
async def get_number_of_order_items(session: SessionDep):
    result = await service.get_number_of_order_items(session)
    return result


@router.get("/{order_item_id}")
async def get_order_item(order_item_id: int, session: SessionDep):
    order_item = await service.get_order_item(order_item_id, session)
    return order_item

@router.get("/", response_model=List[schemas.OrderItemResponse])
async def get_order_items(session: SessionDep):
    order_items = await service.get_order_items(session)
    return order_items