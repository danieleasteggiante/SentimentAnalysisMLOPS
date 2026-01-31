import httpx
from fastapi.params import Depends
from typing import Annotated, List
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from config.constants import TRAINER_URL
from config.database import get_db
from config.logger import logging
from model.feedback import Feedback
from datetime import datetime

LOGGER = logging.getLogger(__name__)
router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]
templates = Jinja2Templates(directory="templates") 


@router.get("/index")
def index(request: Request, db: db_dependency, from_date: str = None, to_date: str = None):
    if from_date is not None or to_date is not None:
        result = db.query(Feedback).filter(Feedback.created_at >= datetime.fromisoformat(from_date), Feedback.created_at <= datetime.fromisoformat(to_date)).all()
        return templates.TemplateResponse("index.html", {"request": request, "feedbacks": result})
    result = db.query(Feedback).all()
    return templates.TemplateResponse("index.html", {"request": request, "feedbacks": result})


@router.get("/edit-label/{feedback_id}/{new_label}")
def edit_label(db: db_dependency, feedback_id: str, new_label: str):
    LOGGER.info(f"Editing label for feedback ID {feedback_id} to {new_label}")
    feedback_entry = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback_entry:
        return JSONResponse(content={"error": "Feedback entry not found"}, status_code=404)
    feedback_entry.labels = new_label
    db.commit()
    return JSONResponse(content={"labels": feedback_entry.labels})

@router.get("/start-trainer")
async def index(request: Request, db: db_dependency, from_date: str = None, to_date: str = None):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{TRAINER_URL}/api/train",timeout=10.0)

        if resp.status_code == 200:
            prediction = resp.json().get("message")
            return JSONResponse(status_code=200, content={"prediction": prediction})

        return JSONResponse(status_code=resp.status_code, content={"message": "Error from trainer server"})




