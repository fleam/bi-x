from fastapi import APIRouter
from app.api.v1.permissions import endpoints

router = APIRouter()
router.include_router(endpoints.router, prefix="", tags=["permissions"])
