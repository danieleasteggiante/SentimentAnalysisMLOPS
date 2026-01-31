import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://admin:admin@localhost:5555/prediction')
TRAINER_URL = os.getenv('TRAINER_URL', 'http://localhost:8505')
