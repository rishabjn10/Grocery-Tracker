from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    order_day = Column(Integer, nullable=True)
    order_month = Column(Integer, nullable=True)
    order_year = Column(Integer, nullable=True)

    total_amount = Column(Numeric(10, 2), nullable=False)

    # TODO: Add payment method column enum
    payment_method = Column(String, nullable=True)
    # TODO: Add order source column enum
    order_source = Column(String, nullable=True)
    discount = Column(Numeric(10, 2), default=0.00)
    final_price = Column(Numeric(10, 2), nullable=False)

    user = relationship("User", back_populates="orders")
    items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    item_name = Column(String, nullable=False)
    # TODO: Add item category column enum
    category = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
