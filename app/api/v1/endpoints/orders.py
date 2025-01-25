import os
import shutil
import tempfile

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.order import OrderResponse
from app.services.order_service import get_order_by_id, process_order_screenshot

router = APIRouter()


@router.post("/upload")
async def upload_order_screenshot(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Upload order screenshot, process it, and remove the temp file."""
    try:
        # Create a temporary file to store the uploaded image
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f"_{file.filename}"
        ) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name  # Get the full path of the temp file

        # Process the uploaded screenshot using OCR and LLM
        order = process_order_screenshot(
            db, temp_file_path, current_user.get("user_id")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

    finally:
        # Ensure the temporary file is deleted after processing
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return order


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_order_by_id(db, order_id, current_user.get("user_id"))
