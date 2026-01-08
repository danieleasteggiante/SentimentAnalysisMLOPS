from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://root:root@localhost:5433/prediction')

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

connection = engine.connect()
print("Database connection established")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

