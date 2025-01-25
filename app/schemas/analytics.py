from pydantic import BaseModel


class TotalSpendingResponse(BaseModel):
    user_id: int
    total_spent: float


class CategorySpendingResponse(BaseModel):
    category: str
    total_spent: float


class MonthlySpendingResponse(BaseModel):
    month: str
    total_spent: float


class PaymentMethodDistributionResponse(BaseModel):
    payment_method: str
    total_spent: float


class TopItemsResponse(BaseModel):
    item_name: str
    total_quantity: int
    total_spent: float


class PlatformSpendingResponse(BaseModel):
    platform: str
    total_spent: float
