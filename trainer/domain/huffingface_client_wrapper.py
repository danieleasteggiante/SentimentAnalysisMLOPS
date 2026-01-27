from config.logger import logging
import os
from huggingface_hub import HfApi, login, create_repo
from pathlib import Path

LOGGER = logging.getLogger(__name__)

class Huggingface_client_wrapper:

    def __init__(self):
        self.api = HfApi()
        
    def __get_repo_id(self):
        user_info = self.api.whoami()
        username = user_info['name']
        self.repo_id = f"{username}/{self.model_name}"

    def __login(self):
        token = os.getenv("HUGGINGFACE_HUB_TOKEN")
        if not token:
            raise ValueError("Huggingface Hub token not found.")
        login(token=token)
        LOGGER.info("Logged in to Huggingface Hub successfully.")
    
    def upload_model(self, model_path: str, model_name: str, version: int):
        self.__initialize_args(model_path, model_name, version)
        LOGGER.info(f"Uploading model to {self.repo_id} (version {self.version})...") 
        create_repo(repo_id=self.repo_id, exist_ok=True, repo_type="model", private=False)
        commit_message = f"Upload model version {self.version}"
        self.__upload_files(commit_message)
        self.__create_tag(commit_message)       
        model_url = f"https://huggingface.co/{self.repo_id}"
        LOGGER.info(f"Model successfully uploaded to {model_url}")
        return model_url
    
    def __upload_files(self, file_path: str, repo_id: str, commit_message: str):
        self.api.upload_file(
            path_or_fileobj=file_path,
            path_in_repo=Path(file_path).name,
            repo_id=repo_id,
            commit_message=commit_message,
            repo_type="model"
        )
        LOGGER.info(f"Uploaded file {file_path} to {repo_id} with message: {commit_message}")
    
    def __create_tag(self):
        self.api.create_tag(
                repo_id=self.repo_id,
                tag=f"v{self.version}",
                tag_message=f"Version {self.version}",
                repo_type="model"
        )
        LOGGER.info(f"Created tag v{self.version} for {self.repo_id} with message: Version {self.version}")

    def __initialize_args(self, model_path: str, model_name: str, version: int):
        self.model_path = model_path
        self.model_name = model_name
        self.version = version
        self.__get_repo_id()
        self.__login()