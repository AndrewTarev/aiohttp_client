from fastapi import APIRouter
from src.api.fastapi_views.coin_info_view import router as coin_router

router = APIRouter()

router.include_router(coin_router)
