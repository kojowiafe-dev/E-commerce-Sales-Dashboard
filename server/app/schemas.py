# from sqlmodel import SQLModel, Field
# from datetime import datetime, date
# from typing import List
# from uuid import uuid4
# from pydantic import EmailStr

# # -----------------------
# # Product Schemas
# # -----------------------


    
    
    
# # -----------------------
# # OrderItem Schemas
# # -----------------------
    
# class OrderItemBase(SQLModel):
#     quantity: int
#     price_each: float
#     line_total: float

# class OrderItemCreate(OrderItemBase):
#     product_id: int

# class OrderItemResponse(OrderItemBase):
#     order_item_id: int
#     product: ProductResponse   # nested product info

#     class Config:
#         orm_mode = True
    
        
        
# # class TokenData(SQLModel):
# #     username: Optional[str] = None


# # class Token(SQLModel):
# #     access_token: str
# #     token_type: str
# #     role: str

# class ForgotPasswordRequest(SQLModel):
#     email: EmailStr