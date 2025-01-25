from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.services.analytics_service import (get_category_wise_spending,
                                            get_monthly_spending_trend,
                                            get_payment_method_distribution,
                                            get_platform_wise_spending,
                                            get_top_ordered_items,
                                            get_total_spending)

router = APIRouter()


@router.get("/total-spending")
def total_spending(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_total_spending(db, current_user.get("user_id"))


@router.get("/category-spending")
def category_spending(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_category_wise_spending(db, current_user.get("user_id"))


@router.get("/monthly-spending")
def monthly_spending(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return get_monthly_spending_trend(db, current_user.get("user_id"))
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch monthly spending data",
        )


@router.get("/payment-method-distribution")
def payment_method_distribution(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_payment_method_distribution(db, current_user.get("user_id"))


@router.get("/top-items")
def top_items(
    top_n: int = 5,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_top_ordered_items(db, current_user.get("user_id"), min(top_n, 50))


@router.get("/platform-spending")
def platform_spending(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_platform_wise_spending(db, current_user.get("user_id"))
