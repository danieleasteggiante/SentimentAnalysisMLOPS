from config.logger import logging
LOGGER = logging.getLogger(__name__)
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,)

class Downloader:
        
    def download(self, model, revision, destination_path):
        LOGGER.info(f"Downloading from {model} {revision} to {destination_path}")
        tokenizer = AutoTokenizer.from_pretrained(model, revision=revision)
        model = AutoModelForSequenceClassification.from_pretrained(model, revision=revision)
        self.__save_model(model, tokenizer, destination_path)
        LOGGER.info("Download completed")
        return tokenizer, model
    
    def __save_model(self, model, tokenizer, destination_path):
        LOGGER.info(f"Saving model to {destination_path}")
        model.save_pretrained(destination_path)
        tokenizer.save_pretrained(destination_path)
        LOGGER.info(f"Model saved to {destination_path}")