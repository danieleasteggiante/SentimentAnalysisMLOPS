from config.logger import logging
LOGGER = logging.getLogger(__name__)
import os
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,)

class Downloader:
        
    def download(self, model, revision, destination_path):
        LOGGER.info(f"Downloading from {model} {revision} to {destination_path}")
        if self.__is_already_downloaded(model, destination_path):
            return self.__load_existing_model(destination_path)
        return self.__downloaded_model(model, revision, destination_path)

    def __save_model(self, model, tokenizer, destination_path):
        LOGGER.info(f"Saving model to {destination_path}")
        model.save_pretrained(destination_path)
        tokenizer.save_pretrained(destination_path)
        LOGGER.info(f"Model saved to {destination_path}")

    def __is_already_downloaded(self, model, destination_path):
        return os.path.exists(destination_path + '/' + model + '*')

    def __load_existing_model(self, destination_path):
        LOGGER.info(f"Loading existing model from {destination_path}")
        return self.__model_from_source(destination_path)

    def __downloaded_model(self, model_name, revision, destination_path):
        LOGGER.info(f"Downloading model {model_name} revision {revision}")
        tokenizer, model = self.__model_from_source(model_name, revision)
        self.__save_model(model, tokenizer, destination_path)
        return tokenizer, model

    def __model_from_source(self, model_name, revision=None):
        LOGGER.info(f"Loading model {model_name} revision {revision} from source")
        tokenizer = AutoTokenizer.from_pretrained(model_name, revision=revision)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, revision=revision)
        return tokenizer, model