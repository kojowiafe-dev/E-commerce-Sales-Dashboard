# routers/orders/schemas.py
from typing import TYPE_CHECKING, List
from sqlmodel import SQLModel
from ..shared.schemas import OrderBase

if TYPE_CHECKING:
    # only for type checkers / IDEs — prevents runtime circular import
    from ..orderitems.schemas import OrderItemCreate, OrderItemInOrderResponse


class OrderCreate(OrderBase):
    # use a stringified List[...] to avoid importing OrderItemCreate at runtime
    items: "List[OrderItemCreate]"

    class Config:
        from_attributes = True


class OrderResponse(OrderBase):
    order_id: int
    items: "List[OrderItemInOrderResponse]"  # forward reference as string

    class Config:
        from_attributes = True


class PaginatedOrders(SQLModel):
    items: "List[OrderResponse]"
    total: int



# Explicitly import OrderItemInOrderResponse and rebuild OrderResponse after all models are defined
try:
    from ..orderitems.schemas import OrderItemInOrderResponse
    OrderResponse.model_rebuild(_types_namespace=globals())
except Exception:
    pass

except Exception:
    pass
