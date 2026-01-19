from sqlalchemy import Column, Integer, String

from config.database import Base


class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    feedback_result = Column(String(10), nullable=False)
