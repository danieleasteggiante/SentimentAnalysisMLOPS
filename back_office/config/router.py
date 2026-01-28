from fastapi import APIRouter
from api.back_office_routes import router as static_router

router = APIRouter(prefix='/back-office')
for r in [static_router]:
    router.include_router(r)
