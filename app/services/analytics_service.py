from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models.order import Order, OrderItem
from app.schemas.analytics import (CategorySpendingResponse,
                                   MonthlySpendingResponse,
                                   PaymentMethodDistributionResponse,
                                   PlatformSpendingResponse, TopItemsResponse,
                                   TotalSpendingResponse)


def get_total_spending(db: Session, user_id: int):
    total_spent = (
        db.query(func.sum(Order.final_price)).filter(
            Order.user_id == user_id).scalar()
    )
    return TotalSpendingResponse(user_id=user_id, total_spent=total_spent or 0)


def get_category_wise_spending(db: Session, user_id: int):
    results = (
        db.query(OrderItem.category, func.sum(OrderItem.total_price))
        .join(Order)
        .filter(Order.user_id == user_id)
        .group_by(OrderItem.category)
        .all()
    )
    return [
        CategorySpendingResponse(category=cat, total_spent=amount)
        for cat, amount in results
    ]


def get_monthly_spending_trend(db: Session, user_id: int):
    results = (
        db.query(func.strftime("%Y-%m", Order.order_date),
                 func.sum(Order.final_price))
        .filter(Order.user_id == user_id)
        .group_by(func.strftime("%Y-%m", Order.order_date))
        .all()
    )
    return [
        MonthlySpendingResponse(month=month, total_spent=amount)
        for month, amount in results
    ]


def get_payment_method_distribution(db: Session, user_id: int):
    results = (
        db.query(Order.payment_method, func.sum(Order.final_price))
        .filter(Order.user_id == user_id)
        .group_by(Order.payment_method)
        .all()
    )
    return [
        PaymentMethodDistributionResponse(
            payment_method=method, total_spent=amount)
        for method, amount in results
    ]


def get_top_ordered_items(db: Session, user_id: int, top_n: int = 5):
    results = (
        db.query(
            OrderItem.item_name,
            func.sum(OrderItem.quantity),
            func.sum(OrderItem.total_price),
        )
        .join(Order)
        .filter(Order.user_id == user_id)
        .group_by(OrderItem.item_name)
        .order_by(func.sum(OrderItem.total_price).desc())
        .limit(top_n)
        .all()
    )
    return [
        TopItemsResponse(item_name=item, total_quantity=qty, total_spent=spent)
        for item, qty, spent in results
    ]


def get_platform_wise_spending(db: Session, user_id: int):
    results = (
        db.query(Order.order_source, func.sum(Order.final_price))
        .filter(Order.user_id == user_id)
        .group_by(Order.order_source)
        .all()
    )
    return [
        PlatformSpendingResponse(platform=platform, total_spent=amount)
        for platform, amount in results
    ]
