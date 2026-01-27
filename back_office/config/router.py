from fastapi import APIRouter
from back_office.api.back_office_routes import router as static_router

router = APIRouter(prefix='/back_office')
for r in [static_router]:
    router.include_router(r)
