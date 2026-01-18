import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from config.logger import logging
from entity.ModelVersion import ModelVersion

LOGGER = logging.getLogger(__name__)

tokenizer = None
model = None
sentiment = None

async def __load_model(db):
    global tokenizer, model, sentiment
    if sentiment is not None:
        return
    MODEL_NAME = await __get_model_name(db)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    model.to(torch.device("cpu"))
    model.eval()
    sentiment = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=-1)

async def inference(db, text):
    await __load_model(db)
    result = sentiment(text)
    LOGGER.info(result)
    return result

async def __get_model_name(db):
    result = db.query(ModelVersion).order_by(ModelVersion.version.desc()).first()
    if result.version is None:
        return f"{result.model_name}"
    return f"{result.model_name}_v{result.version}"