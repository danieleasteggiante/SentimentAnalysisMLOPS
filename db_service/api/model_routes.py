from fastapi.params import Depends
from typing import Annotated
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from config.database import get_db
from config.logger import logging

LOGGER = logging.getLogger(__name__)
router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]
templates = Jinja2Templates(directory="templates")  # crea la cartella `templates`


@router.get("/all/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Ciao da FastAPI"})



@router.get("/id/")
def index(request: Request):
    return templates.TemplateResponse("contacts.html", {"request": request, "message": "Daniele Asteggiante"})








