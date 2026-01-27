from fastapi.params import Depends
from typing import Annotated, List
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from back_office.model.feedback_response import FeedbackResponse
from config.constants import MODEL_SERVER_URL
from config.database import get_db
from config.logger import logging
from model.feedback import Feedback
from datetime import datetime

LOGGER = logging.getLogger(__name__)
router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]
templates = Jinja2Templates(directory="templates")  # crea la cartella `templates`


@router.get("/index/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Ciao da FastAPI"})

@router.get("/predictions/{from_date}/{to_date}", response_model=List[FeedbackResponse])
def get_predictions(from_date: datetime, to_date: str, db: db_dependency):
    LOGGER.info(f"Fetching predictions from {from_date} to {to_date}")
    from_dt = datetime.fromisoformat(from_date) or datetime.min
    to_dt = datetime.fromisoformat(to_date) or datetime.max    
    return db.query(Feedback).filter(Feedback.created_at >= from_dt, Feedback.created_at <= to_dt).all()


@router.post("/edit-label/")
def edit_label(feedback_id: int, new_label: str, db: db_dependency):
    LOGGER.info(f"Editing label for feedback ID {feedback_id} to {new_label}")
    feedback_entry = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback_entry:
        return JSONResponse(content={"error": "Feedback entry not found"}, status_code=404)
    feedback_entry.label = new_label
    db.commit()
    return JSONResponse(content={"message": "Label updated successfully"})





