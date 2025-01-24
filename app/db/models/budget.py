from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    monthly_budget = Column(Numeric(10, 2), nullable=False)
    weekly_budget = Column(Numeric(10, 2), nullable=False)

    user = relationship("User", back_populates="budgets")


class ExpenseAnalysis(Base):
    __tablename__ = "expense_analysis"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String, nullable=False)
    monthly_limit = Column(Numeric(10, 2), nullable=False)
    weekly_limit = Column(Numeric(10, 2), nullable=False)
    monthly_spent_alert_triggered = Column(Boolean, default=False)
    weekly_spent_alert_triggered = Column(Boolean, default=False)
