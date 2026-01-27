from datasets import load_dataset
from config.constant import EVALUATION_STRATEGY, LEARNING_RATE, MODEL_SAVE_PATH, NUM_TRAIN_EPOCHS, PER_DEVICE_EVAL_BATCH_SIZE, PER_DEVICE_TRAIN_BATCH_SIZE, RANDOM_SEED, RESULTS_DIR, TRAIN_DATA_PATH, WEIGHT_DECAY
from entity.Feedback import Feedback
from domain.csv_parser import CSV_parser
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    DataCollatorWithPadding,
    TrainingArguments,
    Trainer,
    pipeline,
)
import evaluate
from sklearn.model_selection import train_test_split
import numpy as np
from config.logger import logging
from entity.ModelVersion import ModelVersion
from domain.downloader import Downloader

LOGGER = logging.getLogger(__name__)

class TrainerWrapper:
    def __init__(self, db, downloader: Downloader, csv_parser: CSV_parser):
        self.db = db
        self.downloader = downloader
        self.csv_parser = csv_parser
        self.__metrics_results = {"current": {}, "new": {}}
        self.__load_component()

    def __load_component(self):
        self.__download_model_and_tokenizer()
        self.__parsing_in_csv()
        self.__load_dataset()
        self.__tokenize()
        self.__load_metrics_functions()
        self.__evaluate()

    def __evaluate(self, dataset_name="test", metrics_step="current"):
        LOGGER.info(f"Evaluating {metrics_step} model on {dataset_name} dataset.")
        trainer = Trainer(model=self.model, tokenizer=self.tokenizer, compute_metrics=self.__compute_metrics)
        eval_results = trainer.evaluate(self.tokenized[dataset_name])
        self.__metrics_results[metrics_step] = {
            "accuracy": eval_results.get("eval_accuracy", 0),
            "f1_macro": eval_results.get("eval_f1_macro", 0),
            "loss": eval_results.get("eval_loss", 0),
        }
    
    def __load_metrics_functions(self):
        LOGGER.info("Setting up evaluation metrics.")
        self.accuracy = evaluate.load("accuracy")
        self.f1 = evaluate.load("f1")
        LOGGER.info("Evaluation metrics set up successfully.")

    def __tokenize(self):
        LOGGER.info("Tokenizing dataset for training.")
        self.tokenized = {
            split: self.dataset[split].map(self.__preprocess, batched=True, remove_columns=["text"])
            for split in ["train", "validation", "test"]
        }

    def __split_dataset(self, full_dataset, treshold=0.3):
        train_test = full_dataset.train_test_split(test_size=treshold, seed=RANDOM_SEED)
        return train_test["train"], train_test["test"]

    def __load_dataset(self):
        LOGGER.info("Loading dataset from CSV for training.")
        full_dataset = load_dataset("csv", data_files=TRAIN_DATA_PATH)["train"]
        train_val, test = self.__split_dataset(full_dataset)
        train, val = self.__split_dataset(train_val, treshold=0.2)
        self.dataset = { "train": train, "validation": val, "test": test}
        LOGGER.info(f"Dataset split: train={len(train)}, val={len(val)}, test={len(test)}")

    def __parsing_in_csv(self):
        LOGGER.info("Parsing data from database to CSV for training.")
        query_result = self.__get_data_from_db()
        self.csv_parser.parse(query_result, TRAIN_DATA_PATH)

    def __get_data_from_db(self):
        LOGGER.info("Fetching data from the database for training.")
        return self.db.query(Feedback).where(Feedback.feedback_result == 'LIKED').all()

    def __download_model_and_tokenizer(self):
        LOGGER.info("Downloading model and tokenizer.")
        self.model = self.__get_model_name()
        self.tokenizer, self.model = self.downloader.download(model_uri=self.model.model_name, model_version=self.model.version, destination_path=MODEL_SAVE_PATH)

    def __get_model_name(self):
        LOGGER.info("Fetching the latest model version from the database.")
        return self.db.query(ModelVersion).order_by(ModelVersion.version.desc()).first()

    def __preprocess(self, batch):
        return self.tokenizer(batch["text"], truncation=True, padding="longest")

    def __compute_metrics(self, eval_pred):
        logits, labels = eval_pred
        preds = np.argmax(logits, axis=-1)
        return {
            "accuracy": self.accuracy.compute(predictions=preds, references=labels)["accuracy"],
            "f1_macro": self.f1.compute(predictions=preds, references=labels, average="macro")["f1"],
        }

    def train(self):
        LOGGER.info("Starting model training.")
        data_collator = DataCollatorWithPadding(self.tokenizer)
        training_args = self.__get_training_args()
        self.trainer = self.__get_trainer(training_args, data_collator)
        self.trainer.train()
        self.__evaluate(metrics_step="new")

    def persist_model(self, huggingface_client_wrapper):
        LOGGER.info("Comparing current and new model metrics.")
        current_metrics = self.__metrics_results["current"]
        new_metrics = self.__metrics_results["new"]
        LOGGER.info(f"Current Model Metrics: {current_metrics} - New Model Metrics: {new_metrics}")
        
        if new_metrics["accuracy"] > current_metrics["accuracy"]:
            LOGGER.info("New model outperforms the current model. Saving new model.")
            self.__save_model(huggingface_client_wrapper)
            return True
        
        LOGGER.info("New model does not outperform the current model. Discarding new model.")
        return False

    def __save_model(self, huggingface_client_wrapper):
        LOGGER.info("Saving the new model to the database and local storage.")
        self.trainer.save_model(f"{self.PATH}/{self.FILE_NAME}_v{self.version + 1}")
        self.db.save(ModelVersion(model_name=self.FILE_NAME, version=self.version + 1))
        self.db.commit()
        huggingface_client_wrapper.upload_model(
            model_path=f"{self.PATH}/{self.FILE_NAME}_v{self.version + 1}",
            model_name=self.FILE_NAME,
            version=self.version + 1,
        )
        LOGGER.info("New model saved successfully.")

    def __get_training_args(self):
        return TrainingArguments(
            output_dir=RESULTS_DIR,
            evaluation_strategy=EVALUATION_STRATEGY,
            learning_rate=LEARNING_RATE,
            per_device_train_batch_size=PER_DEVICE_TRAIN_BATCH_SIZE,
            per_device_eval_batch_size=PER_DEVICE_EVAL_BATCH_SIZE,
            num_train_epochs=NUM_TRAIN_EPOCHS,
            weight_decay=WEIGHT_DECAY,
        )
    
    def __get_trainer(self, training_args, data_collator):
        return Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.tokenized["train"],
            eval_dataset=self.tokenized["validation"],
            tokenizer=self.tokenizer,
            data_collator=data_collator,
            compute_metrics=self.__compute_metrics,
        )