from fastapi import FastAPI

from config import database
from config.database import engine
from config.router import router

app = FastAPI()
app.include_router(router)

database.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Model training is running"}