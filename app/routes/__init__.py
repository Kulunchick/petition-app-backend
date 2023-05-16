from fastapi import APIRouter

from app.routes import v1

router = APIRouter(prefix="/api")

router.include_router(v1.router)
