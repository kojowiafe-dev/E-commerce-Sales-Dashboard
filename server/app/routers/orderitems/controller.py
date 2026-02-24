from fastapi import APIRouter
from ...routers.orderitems import schemas, service
from ...database.core import SessionDep


router = APIRouter(
    prefix="/order-items", 
    tags=["Order Items"]
)


@router.get("/total-order-items")
async def get_number_of_order_items(session: SessionDep):
    result = await service.get_number_of_order_items(session)
    return result


# @router.get()
# async def


@router.get("/{order_item_id}", response_model=schemas.OrderItemResponse)
async def get_order_item(order_item_id: int, session: SessionDep):
    order_item = await service.get_order_item(order_item_id, session)
    return order_item

@router.get("/", response_model=schemas.PaginatedOrderItems)
async def get_order_items(
    session: SessionDep,
    page: int = 1,
    limit: int = 10,
    search: str | None = None
):
    return await service.get_order_items(session, page, limit, search)
