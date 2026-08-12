from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.FeedbackResponse)
def create_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    if feedback.rating not in {1, 2, 3, 4, 5}:
        raise HTTPException(status_code=422, detail="Choose a rating from 1 to 5.")
    comment = (feedback.comment or "").strip()
    if len(comment) > 1000:
        raise HTTPException(status_code=422, detail="Keep feedback under 1,000 characters.")
    record = models.Feedback(
        rating=feedback.rating,
        category=feedback.category,
        comment=comment or None,
        created_at=datetime.now(timezone.utc),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"id": record.id, "message": "Thank you — your feedback was saved."}
