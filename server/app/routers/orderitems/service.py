from fastapi import HTTPException, status
from sqlalchemy import func, or_
from sqlmodel import String, cast, select
from ...database.core import SessionDep
from ...models.model import OrderItem, Order
from sqlalchemy.orm import selectinload
from ..orderitems import schemas


async def get_total_revenue(session: SessionDep):
    result = await session.execute(select(func.sum(OrderItem.line_total)))
    total_revenue = result.scalar() or 0.0
    return {"total_revenue": f"{total_revenue:.2f}"}


async def get_revenue_trend(session: SessionDep):
    query = (
        select(
            func.date_trunc(
                "month",
                func.to_timestamp(Order.order_date, "MM/DD/YY HH24:MI")  # cast string -> timestamp
            ).label("month"),
            func.sum(OrderItem.line_total).label("revenue")
        )
        .join(Order.items)
        .group_by("month")
        .order_by("month")
    )

    result = await session.execute(query)

    return [
        {"month": row.month.strftime("%Y-%m"), "revenue": float(row.revenue)}
        for row in result
    ]


async def get_sales_by_city(session: SessionDep, limit: int = 5):
    query = (
        select(
            func.substr(
                Order.purchase_address,
                func.strpos(Order.purchase_address, ",") + 2,  # find first comma
                50
            ).label("city"),
            func.sum(OrderItem.line_total).label("revenue")
        )
        .join(Order.items)
        .group_by("city")
        .order_by(func.sum(OrderItem.line_total).desc())
        .limit(limit)
    )
    result = await session.execute(query)
    return [{"city": row.city.strip(), "revenue": float(row.revenue)} for row in result]


async def get_number_of_order_items(session: SessionDep):
    result = await get_order_items(session)
    return {"number of order items": str(len(result))}


async def get_order_item(order_item_id: str, session: SessionDep):
    stmt = (
        select(OrderItem)
        .options(
            selectinload(OrderItem.product),
            selectinload(OrderItem.order).selectinload(Order.items)
        )
        .where(OrderItem.order_item_id == order_item_id)
    )
    result = await session.execute(stmt)
    order_item = result.scalar_one_or_none()

    if not order_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order_item not found")

    return order_item


async def get_order_items(session: SessionDep, page: int, limit: int, search: str | None = None):
    offset = (page - 1) * limit

    query = (
        select(OrderItem)
        .options(
            selectinload(OrderItem.product),
            selectinload(OrderItem.order).selectinload(Order.items)
        )
    )

    if search:
        filters = []
        if search.isdigit():
            # Exact match if numeric
            filters.append(OrderItem.order_id == int(search))
            # Optional: allow partial match by casting
            filters.append(cast(OrderItem.order_id, String).ilike(f"%{search}%"))

        # Search in text fields too
        filters.append(OrderItem.purchase_address.ilike(f"%{search}%"))

        query = query.where(or_(*filters))

    orders = await session.execute(
        query.order_by(OrderItem.order_id).offset(offset).limit(limit)
    )
    orders = orders.scalars().all()

    total_query = select(func.count()).select_from(OrderItem)
    if search:
        total_query = total_query.where(or_(*filters))

    total = await session.scalar(total_query)

    return schemas.PaginatedOrderItems(
        total=total,
        page=page,
        limit=limit,
        items=[schemas.OrderItemResponse.from_orm(o) for o in orders]
    )
