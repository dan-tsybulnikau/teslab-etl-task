from fastapi import APIRouter, Depends

from app.api.api_v1.endpoint.url import router as api_v1_router



router = APIRouter()
router.include_router(api_v1_router)

