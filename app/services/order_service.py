from app.schemas.order import OrderResponse, OrderItem
from sqlalchemy.orm import Session
from app.db.models.order import Order, OrderItem
from app.utils.openai import parse_order_screenshot


def process_order_screenshot(db: Session, image_path: str, user_id: int) -> OrderResponse:
    """Extract and process order details using OCR and LLM."""

    # Send extracted text to LLM for structured parsing
    extracted_data: dict = parse_order_screenshot(image_path)

    order = Order(
        user_id=user_id,
        order_date=extracted_data.get("order_date"),
        total_amount=extracted_data.get("total_price"),
        payment_method=extracted_data.get("payment_method"),
        order_source=extracted_data.get("order_source"),
        final_price=extracted_data.get("final_price"),
        discount=extracted_data.get("discount"),
    )

    db.add(order)
    db.flush()  # Get order ID before adding items

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

    db.commit()
    db.refresh(order)
    return extracted_data  # order
