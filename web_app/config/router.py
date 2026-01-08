from fastapi import APIRouter
from web_app.api.basic_routes import router as basic_router

router = APIRouter(prefix='/api')
for r in [basic_router]:
    router.include_router(r)
