from http.client import HTTPResponse

from fastapi import FastAPI
from starlette.responses import JSONResponse

from config import database
from config.database import engine
from config.router import router

app = FastAPI()
app.include_router(router)

database.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root() -> JSONResponse:
    return JSONResponse(status_code=200, content="OK", headers={"X-App-Version": "1.0"})
