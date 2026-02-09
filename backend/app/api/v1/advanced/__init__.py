from fastapi import APIRouter
from app.api.v1.advanced import endpoints

router = APIRouter()
router.include_router(endpoints.router, prefix="", tags=["advanced"])
