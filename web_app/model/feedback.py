from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from config.database import Base

class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    message_text = Column(String(4000), nullable=False)
    label = Column(String(50), nullable=False)
    feedback_result = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
