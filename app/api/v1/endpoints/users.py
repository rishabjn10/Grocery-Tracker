from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, get_current_user
from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.services.user_service import (authenticate_user, create_user,
                                       get_user_by_id, update_user)

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.get("/", response_model=UserResponse)
def get_user(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return get_user_by_id(db, current_user.get("user_id"))


@router.put("/", response_model=UserResponse)
def update_user_info(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_user(db, current_user.get("user_id"), user_data)


@router.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_credentials.email,
                             user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id,
              "user_name": user.full_name},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
