import asyncio
from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi.responses import JSONResponse
from config.database import get_db
from config.logger import logging

LOGGER = logging.getLogger(__name__)
router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]

user_service_dependency = Annotated[UserService,Depends(get_user_service)]

@router.post("/api/")
async def login_user(db: db_dependency, us : user_service_dependency, user: UserSerializer) -> JSONResponse:
    try:
        LOGGER.info("Login user")
        email, password = user.email, user.password
        existing_user = await us.get_user_if_exists(db, email, password)
        if existing_user:
            return await us.handle_existing_user(existing_user)
        return JSONResponse(status_code=404, content={"message": "User not found"})
    except ChildProcessError as e:
        LOGGER.error("Error logging in user: %s", e)
        return JSONResponse(status_code=404, content={"message": "Error logging in user"})








