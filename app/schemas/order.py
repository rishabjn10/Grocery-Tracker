from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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

class OrderResponse(BaseModel):
    order_id: int
    vendor: str
    order_date: datetime
    payment_method: str
    total_amount: float
    items: List[OrderItem]

    class Config:
        orm_mode = True

# Spending pattern response
class SpendingPatternResponse(BaseModel):
    category: str
    total_spent: float
    frequency: int
    average_spent_per_order: float
