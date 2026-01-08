from fastapi import FastAPI

from config import database
from config.database import engine
from config.router import router

app = FastAPI()
app.include_router(router)
app.add_middleware(allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"], )
database.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Celiac Predictor API is running"}