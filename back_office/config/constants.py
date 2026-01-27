import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://admin:admin@localhost:5555/prediction')
MODEL_SERVER_URL = os.getenv('MODEL_SERVER_URL', 'http://localhost:8501')
