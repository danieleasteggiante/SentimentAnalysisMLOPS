from datetime import datetime
from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class ModelVersion(Base):
    __tablename__ = 'model_versions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(100), nullable=False)
    version = Column(Integer, nullable=False)
    registration_date = Column(DateTime, default=datetime.now)