from fastapi.params import Depends
from typing import Annotated
from fastapi import APIRouter
from sqlalchemy.orm import Session

from domain.trainer import TrainerWrapper
from services.download import download_and_save_model

from config.database import get_db
from config.logger import logging

LOGGER = logging.getLogger(__name__)
router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/train")
async def index(db: db_dependency):
    try:
        trainer = TrainerWrapper(db)
        trainer.train()
        return trainer.evaluate()
    except Exception as e:
        LOGGER.error("Error training model: %s", e)
        return {"message": "Error training model"}

@router.get("/download")
async def index(db: db_dependency):
    try:
        LOGGER.info("Downloading model")
        download_and_save_model(db)
        return {"message": "Model downloaded successfully"}
    except Exception as e:
        LOGGER.error("Error downloading model: %s", e)
        return {"message": "Error downloading model"}




