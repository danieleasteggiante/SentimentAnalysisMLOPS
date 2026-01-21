import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from config.logger import logging
from entity.ModelVersion import ModelVersion

LOGGER = logging.getLogger(__name__)

async def __load_model(db):
    model_name = await __get_model_name(db)
    return pipeline("sentiment-analysis", model=model_name, device=-1)

async def inference(db, text):
    sentiment = await __load_model(db)
    result = sentiment(text)
    LOGGER.info(result)
    return result

async def __get_model_name(db):
    result = db.query(ModelVersion).order_by(ModelVersion.version.desc()).first()
    if result.version is None:
        return f"{result.model_name}"
    return f"{result.model_name}_v{result.version}"