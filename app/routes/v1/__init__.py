from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.routes.v1 import votes, users, auth, petitions

router = APIRouter(prefix="/v1")

router.include_router(petitions.router)
router.include_router(auth.router)
router.include_router(users.router)
router.include_router(votes.router)


@router.get("/")
async def get_api():
    return JSONResponse(
        status_code=200,
        content={
            "version": 1.0
        }
    )
