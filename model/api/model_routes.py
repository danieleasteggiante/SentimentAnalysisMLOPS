from fastapi.params import Depends
from typing import Annotated
from fastapi import APIRouter
from sqlalchemy.orm import Session

from entity.InferenceRequest import InferenceRequest
from services.inference import inference
from services.inference import unload_pipeline

from config.database import get_db
from config.logger import logging

LOGGER = logging.getLogger(__name__)
router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/inference")
async def index(db: db_dependency, data: InferenceRequest):
    try:
        LOGGER.info("Testing model")
        result = await inference(db, data.text)
        return {"message": result}
    except Exception as e:
        LOGGER.error("Error testing model: %s", e)
        return {"message": "Error testing model"}

@router.get("/unload_model")
async def unload_model():
    try:
        LOGGER.info("Unloading model")
        await unload_pipeline()
        return {"message": "Model unloaded successfully"}
    except Exception as e:
        LOGGER.error("Error unloading model: %s", e)
        return {"message": "Error unloading model"}


