from datetime import datetime
from typing import List

from pydantic import BaseModel


# Request schema for image upload
class OrderUpload(BaseModel):
    filename: str
    content_type: str
    upload_time: datetime


class OrderItem(BaseModel):
    item_name: str
    quantity: int
    unit_price: float
    total_price: float


class OrderItemResponse(BaseModel):
    id: int
    item_name: str
    category: str
    quantity: int
    unit_price: float
    total_price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    order_day: int | None
    order_month: int | None
    order_year: int | None
    total_amount: float
    payment_method: str | None
    order_source: str | None
    final_price: float
    discount: float
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True


# Spending pattern response


class SpendingPatternResponse(BaseModel):
    category: str
    total_spent: float
    frequency: int
    average_spent_per_order: float
