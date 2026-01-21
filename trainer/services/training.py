from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    DataCollatorWithPadding,
    TrainingArguments,
    Trainer,
    pipeline,
)
import evaluate
import numpy as np
from config.logger import logging
from entity.ModelVersion import ModelVersion

LOGGER = logging.getLogger(__name__)

class TrainModel:
    def __init__(self, db):
        self.db = db
        self.model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.data_files = {"train": "train.csv", "validation": "val.csv"}
        self.ds = load_dataset("csv", data_files=self.data_files)
        self.num_labels = len(set(self.ds["train"]["label"]))
        self.tokenized = self.ds.map(self.__preprocess, batched=True, remove_columns=["text"])
        self.accuracy = evaluate.load("accuracy")
        self.f1 = evaluate.load("f1")
        self.version = self.__get_version()
        self.PATH = "../outputs"
        self.FILE_NAME = "model_state"
        LOGGER.info("Num labels dataset:", self.num_labels)
        LOGGER.info("Model num_labels:", self.model.config.num_labels)

    def __get_version(self):
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
        data_collator = DataCollatorWithPadding(self.tokenizer)

        training_args = TrainingArguments(
            output_dir="../outputs",
            save_strategy="epoch",
            per_device_train_batch_size=16,
            per_device_eval_batch_size=32,
            num_train_epochs=3,
            learning_rate=2e-5,
            load_best_model_at_end=True,
            metric_for_best_model="accuracy",
            logging_steps=50,
            save_total_limit=2,
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.tokenized["train"],
            eval_dataset=self.tokenized["validation"],
            tokenizer=self.tokenizer,
            data_collator=data_collator,
            compute_metrics=self.__compute_metrics,
        )

        trainer.train()
        sentiment = self.__save_model(trainer)
        LOGGER.info(sentiment("Covid cases are increasing fast!"))
        LOGGER.info("Model trained and saved successfully.")

    def __save_model(self, trainer):
        trainer.save_model(f"{self.PATH}/{self.FILE_NAME}_v{self.version + 1}")
        self.db.save(ModelVersion(model_name=self.FILE_NAME, version=self.version + 1))
        self.db.commit()
        sentiment = pipeline("sentiment-analysis", model="outputs/best_model", tokenizer=self.tokenizer)
        return sentiment

    def evaluate(self):
        trainer = Trainer(
            model=self.model,
            compute_metrics=self.__compute_metrics,
        )
        results = trainer.evaluate(self.tokenized["validation"])
        LOGGER.info("Evaluation results:", results)



