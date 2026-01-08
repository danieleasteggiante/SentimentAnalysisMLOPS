from fastapi import FastAPI

from config import database
from config.database import engine
from config.router import router as main_router

app = FastAPI()
app.include_router(main_router)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"], )

app.add_middleware(TokenMiddleware)

database.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Celiac Predictor API is running"}