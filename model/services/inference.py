import asyncio

from transformers import pipeline
from config.logger import logging
from entity.ModelVersion import ModelVersion

LOGGER = logging.getLogger(__name__)

_model_name = None
_revision = None
_pipeline = None

async def __load_model(db):
    LOGGER.info("Download pipeline for the first time")
    global _model_name, _revision
    _model_name, _revision = await __get_model_name(db)
    return await asyncio.to_thread(
        lambda: pipeline("sentiment-analysis", model=_model_name, revision=_revision, device=-1)
    )

async def __get_pipeline(db):
    LOGGER.info("Loading model pipeline")
    global _pipeline, _model_name, _revision
    _, current_revision = await __get_model_name(db)
    if _revision != current_revision or _pipeline is None:
        LOGGER.info("Something changed, reloading: model_name=%s, old_revision=%s, new_revision=%s, pipeline_is_none=%s", _model_name, _revision, current_revision, _pipeline is None)
        _pipeline = await __load_model(db)
    return _pipeline

async def inference(db, text):
    sentiment = await __get_pipeline(db)
    result = sentiment(text)
    LOGGER.info(result)
    return result

async def __get_model_name(db):
    result = db.query(ModelVersion).order_by(ModelVersion.registration_date.desc()).first()
    LOGGER.info(f"Using model: {result.model_name} version: {result.version}")
    return result.model_name, result.version

async def unload_pipeline():
    global _pipeline
    LOGGER.info("Unloading model pipeline")
    _pipeline = None