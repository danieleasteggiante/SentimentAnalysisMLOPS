from fastapi import APIRouter
from api.model_routes import router as static_router

router = APIRouter(prefix='/api')
for r in [static_router]:
    router.include_router(r)
