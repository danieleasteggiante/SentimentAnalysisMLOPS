from fastapi.params import Depends
from typing import Annotated
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import httpx
from starlette.responses import JSONResponse

from config.constants import MODEL_SERVER_URL
from config.database import get_db
from config.logger import logging

LOGGER = logging.getLogger(__name__)
router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]
templates = Jinja2Templates(directory="templates")  # crea la cartella `templates`


@router.get("/index/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Ciao da FastAPI"})



@router.get("/contacts/")
def index(request: Request):
    return templates.TemplateResponse("contacts.html", {"request": request, "message": "Daniele Asteggiante"})

@router.post("/predict")
async def predict(request: Request):
    data = await request.json()

    text = data.get("text")
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{MODEL_SERVER_URL}/api/inference", json={"text": text}, timeout=10.0)

    if resp.status_code == 200:
        prediction = resp.json().get("message")
        return JSONResponse(status_code=200, content={"prediction": prediction})

    LOGGER.error("Error from model server: %s", resp.text)
    return JSONResponse(status_code=500, content={"message": "Error from model server"})








