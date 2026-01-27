from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FeedbackResponse(BaseModel):
    id: int
    username: str
    message_text: str
    label: str
    feedback_result: str
    created_at: Optional[datetime]
    
    class Config:
        from_attributes = True