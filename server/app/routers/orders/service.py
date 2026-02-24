from sqlmodel import func, select
from ...database.core import SessionDep
from ...models.model import Order, OrderItem
from sqlalchemy import or_, cast, String
from sqlalchemy.orm import selectinload
from ..orderitems.service import get_revenue_trend, get_sales_by_city, get_total_revenue
from ..products.service import get_top_products
from .schemas import PaginatedOrders, OrderResponse



async def get_summary(session: SessionDep):
    total_orders = await get_number_of_orders(session)
    total_revenue = await get_total_revenue(session)
    top_products = await get_top_products(session)
    revenue_trend = await get_revenue_trend(session)
    sales_by_city = await get_sales_by_city(session)

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "top_products": top_products,
        "revenue_trend": revenue_trend,
        "sales_by_city": sales_by_city,
    }


    

async def get_number_of_orders(session: SessionDep):
    result = await session.execute(select(Order))
    result = result.scalars().all()
    return {"number of orders": str(len(result))}



async def get_order(order_id: int, session: SessionDep):
    result = await session.execute(
        select(Order)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
        .where(Order.order_id == order_id)
    )
    order = result.scalar_one_or_none()
    return order



async def get_orders(session: SessionDep, page: int, limit: int, search: str | None = None):
    offset = (page - 1) * limit

    query = (
        select(Order)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product)  # eager load
        )
    )

    if search:
        filters = []
        if search.isdigit():
            # Exact match if numeric
            filters.append(Order.order_id == int(search))
            # Optional: allow partial match by casting
            filters.append(cast(Order.order_id, String).ilike(f"%{search}%"))

        # Search in text fields too
        filters.append(Order.purchase_address.ilike(f"%{search}%"))

        query = query.where(or_(*filters))

    orders = await session.execute(
        query.order_by(Order.order_id).offset(offset).limit(limit)
    )
    orders = orders.scalars().all()

    total_query = select(func.count()).select_from(Order)
    if search:
        total_query = total_query.where(or_(*filters))

    total = await session.scalar(total_query)

    return PaginatedOrders(
        total=total,
        page=page,
        limit=limit,
        items=[OrderResponse.from_orm(o) for o in orders]
    )
