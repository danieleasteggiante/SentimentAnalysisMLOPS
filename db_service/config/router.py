from fastapi import APIRouter
from api.basic_routes import router as static_router

router = APIRouter(prefix='/db')
for r in [static_router]:
    router.include_router(r)
