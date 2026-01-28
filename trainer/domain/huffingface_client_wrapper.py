from config.constant import MODEL_SAVE_PATH
from config.logger import logging
import os
from huggingface_hub import HfApi, login, create_repo
from pathlib import Path
from dotenv import load_dotenv


LOGGER = logging.getLogger(__name__)

class Huggingface_client_wrapper:

    def __init__(self):
        load_dotenv()
        self.api = HfApi()
        self.model_path = None
        self.model_name = None
        self.version = None
        self.token = None

    def __login(self):
        token = os.getenv("HUGGINGFACE_HUB_TOKEN")
        if not token:
            raise ValueError("Huggingface Hub token not found.")
        login(token=token)
        self.api = HfApi(token=token)
        self.token = token
        LOGGER.info("Logged in to Huggingface Hub successfully.")

    def __get_repo_id(self):
        user_info = self.api.whoami()
        username = user_info.get('name')
        if not username:
            raise RuntimeError("Unable to determine Huggingface username via whoami().")

    def upload_model(self, model_path: str, model_name: str, version: int):
        self.__initialize_args(model_path, model_name, version)
        LOGGER.info(f"Uploading model to {self.model_name} (version {self.version})...")
        self.api.create_repo(repo_id=self.model_name, exist_ok=True, repo_type="model", private=False)
        commit_message = f"Upload model version {self.version}"
        self.__upload_files(self.model_name, commit_message)
        self.__create_tag()
        model_url = f"https://huggingface.co/{self.model_name}"
        LOGGER.info(f"Model successfully uploaded to {model_url}")
        return model_url

    def __upload_files(self, repo_id: str, commit_message: str):
        self.api.upload_folder(
            repo_id=repo_id,
            folder_path=MODEL_SAVE_PATH,
            commit_message=commit_message,
            repo_type="model"
        )
        LOGGER.info(f"Uploaded file {MODEL_SAVE_PATH} to {repo_id} with message: {commit_message}")

    def __create_tag(self):
        self.api.create_tag(
            repo_id=self.model_name,
            tag=f"{self.version}",
            tag_message=f"Version {self.version}",
            repo_type="model"
        )
        LOGGER.info(f"Created tag v{self.version} for {self.model_name} with message: Version {self.version}")

    def __initialize_args(self, model_path: str, model_name: str, version: int):
        self.model_path = model_path
        self.model_name = model_name
        self.version = version
        self.__login()
