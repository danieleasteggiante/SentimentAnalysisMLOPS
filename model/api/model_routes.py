from fastapi.params import Depends
from typing import Annotated
from fastapi import APIRouter, Request
from sqlalchemy.orm import Session

from entity.InferenceRequest import InferenceRequest
from services.inference import inference
from services.training import TrainModel
from services.download import download_and_save_model

from config.database import get_db
from config.logger import logging

LOGGER = logging.getLogger(__name__)
router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/train")
def index(db: db_dependency):
    try:
        trainer = TrainModel(db)
        trainer.train()
        return trainer.evaluate()
    except Exception as e:
        LOGGER.error("Error training model: %s", e)
        return {"message": "Error training model"}

@router.post("/inference")
def index(db: db_dependency, data: InferenceRequest):
    try:
        LOGGER.info("Testing model")
        inference(db, data.text)
        return {"message": "Model tested successfully"}
    except Exception as e:
        LOGGER.error("Error testing model: %s", e)
        return {"message": "Error testing model"}

@router.get("/download")
def index(db: db_dependency):
    try:
        LOGGER.info("Downloading model")
        download_and_save_model(db)
        return {"message": "Model downloaded successfully"}
    except Exception as e:
        LOGGER.error("Error downloading model: %s", e)
        return {"message": "Error downloading model"}




