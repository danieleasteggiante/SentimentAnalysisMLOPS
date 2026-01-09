from pydantic import BaseModel

class InferenceRequest(BaseModel):
    text: str