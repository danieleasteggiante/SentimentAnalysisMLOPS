from datetime import datetime
from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    message_text = Column(String(4000), nullable=False)
    labels = Column(String(50), nullable=False)
    feedback_result = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.now)