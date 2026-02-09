from fastapi import APIRouter
from app.api.v1.data_models import endpoints

router = APIRouter()
router.include_router(endpoints.router)
