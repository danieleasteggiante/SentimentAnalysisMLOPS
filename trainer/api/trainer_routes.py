from fastapi.params import Depends
from typing import Annotated
from fastapi import APIRouter
from sqlalchemy.orm import Session

from domain.trainer import TrainerWrapper

from config.database import get_db
from config.logger import logging
from domain.csv_parser import CSV_parser
from domain.downloader import Downloader
from domain.huffingface_client_wrapper import Huggingface_client_wrapper

LOGGER = logging.getLogger(__name__)
router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/train")
async def index(db: db_dependency):
    try:
        LOGGER.info("Starting model training process.")
        trainerw = __get_trainer_wrapper(db)
        huffingface_client_wrapper = Huggingface_client_wrapper()
        trainerw.train()
        trainerw.persist_model(huffingface_client_wrapper)
        return {"message": "Model trained successfully"}
    except Exception as e:
        LOGGER.error("Error training model: %s", e)
        return {"message": "Error training model"}


def __get_trainer_wrapper(db: Session) -> TrainerWrapper:
    downloader = Downloader()
    csv_parser = CSV_parser(db)
    return TrainerWrapper(db, downloader, csv_parser)
