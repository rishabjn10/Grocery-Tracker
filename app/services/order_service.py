from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.db.models.order import Order, OrderItem
from app.schemas.order import OrderItemResponse, OrderResponse
from app.utils.openai import parse_order_screenshot


def process_order_screenshot(
    db: Session, image_path: str, user_id: int
) -> OrderResponse:
    """Extract and process order details using OCR and LLM."""

    # Send extracted text to LLM for structured parsing
    extracted_data: dict = parse_order_screenshot(image_path)

    extracted_date: dict = extracted_data.get("order_date") or {
        "day": None,
        "month": None,
        "year": None,
    }

    order = Order(
        user_id=user_id,
        order_day=extracted_date.get("day"),
        order_month=extracted_date.get("month"),
        order_year=extracted_date.get("year"),
        total_amount=extracted_data.get("total_price"),
        payment_method=extracted_data.get("payment_method"),
        order_source=extracted_data.get("order_source"),
        final_price=extracted_data.get("final_price"),
        discount=extracted_data.get("discount"),
    )

    db.add(order)
    db.flush()

    order_items = []
    for item in extracted_data.get("items", []):
        order_item = OrderItem(
            order_id=order.id,
            item_name=item.get("item_name"),
            quantity=item.get("quantity"),
            unit_price=item.get("unit_price"),
            category=item.get("category"),
            total_price=item.get("total_price"),
        )
        db.add(order_item)
        order_items.append(order_item)

    db.commit()
    db.refresh(order)
    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        order_day=order.order_day,
        order_month=order.order_month,
        order_year=order.order_year,
        total_amount=order.total_amount,
        payment_method=order.payment_method,
        order_source=order.order_source,
        final_price=order.final_price,
        discount=order.discount,
        items=[
            OrderItemResponse(
                id=item.id,
                item_name=item.item_name,
                category=item.category,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price,
            )
            for item in order_items
        ],
    )


def get_order_by_id(db: Session, order_id: int, user_id: int) -> OrderResponse:
    """Fetch order by ID and ensure it belongs to the current user."""

    # Fetch the order and check if it exists
    order = (
        db.query(Order)
        .filter(and_(Order.id == order_id, Order.user_id == user_id))
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    # Convert order items to response format
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        order_day=order.order_day,
        order_month=order.order_month,
        order_year=order.order_year,
        total_amount=order.total_amount,
        payment_method=order.payment_method,
        order_source=order.order_source,
        final_price=order.final_price,
        discount=order.discount,
        items=[
            OrderItemResponse(
                id=item.id,
                item_name=item.item_name,
                category=item.category,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price,
            )
            for item in order_items
        ],
    )
