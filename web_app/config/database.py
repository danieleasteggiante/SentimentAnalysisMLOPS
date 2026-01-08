from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from web_app.settings import settings

DATABASE_URL = 'postgresql+psycopg2://root:root@localhost:5433/celiac_db'

engine = create_engine(settings.DATABASE_URL, echo=False) #echo=True to see the SQL statements
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

connection = engine.connect()
print("Database connection established", )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

