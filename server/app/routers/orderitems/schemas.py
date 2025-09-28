# routers/orderitems/schemas.py
from typing import TYPE_CHECKING, List
from sqlmodel import SQLModel
from ..shared.schemas import OrderItemBase
from ..products.schemas import ProductResponse

if TYPE_CHECKING:
    # only for type checkers / IDEs — prevents runtime circular import
    from ..orders.schemas import OrderResponse


class OrderItemCreate(OrderItemBase):
    product_id: int

    class Config:
        from_attributes = True
        
        
class OrderItemInOrderResponse(OrderItemBase):
    order_item_id: int
    product: ProductResponse
    
    class Config:
        from_attributes = True


class OrderItemResponse(OrderItemBase):
    order_item_id: int
    product: ProductResponse
    order: "OrderResponse"  # forward reference as string

    class Config:
        from_attributes = True
        
    
class PaginatedOrderItems(SQLModel):
    items: "List[OrderItemResponse]"
    total: int


# Explicitly import OrderResponse and rebuild OrderItemResponse after all models are defined
try:
    from ..orders.schemas import OrderResponse
    OrderItemResponse.model_rebuild(_types_namespace=globals())
except Exception:
    pass
