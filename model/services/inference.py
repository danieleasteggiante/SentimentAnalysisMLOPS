import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from config.logger import logging
from entity.ModelVersion import ModelVersion

LOGGER = logging.getLogger(__name__)

def inference(db, text):
    tokenizer_dir = "../outputs/tokenizer"
    state_path = f"../outputs/model_state_v{__get_model(db)}.pkl"
    base_model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    num_labels = 3
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(base_model_name, num_labels=num_labels)
    state = torch.load(state_path, map_location="cpu")
    model.load_state_dict(state)
    model.eval()
    sentiment = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    result = sentiment(text)
    LOGGER.info(result)
    return result

def __get_model(db):
    return db.query(ModelVersion).order_by(ModelVersion.version.desc()).first()
