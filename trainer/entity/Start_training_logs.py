from datetime import datetime
from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class Start_training_logs(Base):
    __tablename__ = 'start_training_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    feedback_id = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)