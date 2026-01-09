# python
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from config.logger import logging
from entity.ModelVersion import ModelVersion

LOGGER = logging.getLogger(__name__)


def __get_model_name(db):
    model = db.query(ModelVersion).order_by(ModelVersion.version.desc()).first()
    return f"{model.name}_v{model.version}.pkl"



def download_and_save_model(db):
    model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    LOGGER.info("Loading model and tokenizer from:", model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    LOGGER.info("Model loaded with num_labels:", model.config.num_labels)
    model_name = __get_model_name(db)
    torch.save(model.state_dict(), '../outputs/model_state_v0.pkl')
    tokenizer.save_pretrained('outputs/tokenizer')
    LOGGER.info("Model and tokenizer saved to 'outputs/' directory.")

    model2 = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=model.config.num_labels)
    model2.load_state_dict(torch.load('outputs/model_state.pkl', map_location='cpu'))
    model2.eval()
    LOGGER.info("Model reloaded and set to eval mode.")