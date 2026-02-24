from fastapi import APIRouter
from ...routers.orders import schemas, service
from ...database.core import SessionDep



router = APIRouter(
    prefix="/orders", 
    tags=["Orders"]
)


@router.get("/total-orders/")
async def get_number_of_orders(session: SessionDep):
    result = await service.get_number_of_orders(session)
    return result


@router.get("/{order_id}/", response_model=schemas.OrderResponse)
async def get_order(order_id: int, session: SessionDep):
    order = await service.get_order(order_id, session)
    return order


@router.get("/analytics/summary")
async def get_analytics_summary(session: SessionDep):
    summary = await service.get_summary(session)
    return summary


@router.get("/", response_model=schemas.PaginatedOrders)
async def get_orders(
    session: SessionDep,
    page: int = 1,
    limit: int = 10,
    search: str = None
):
    return await service.get_orders(session, page, limit, search)