from fastapi import APIRouter

from app.api.v1.endpoint import order

api_router = APIRouter()

api_router.include_router(order.router, prefix="/order", tags=["order"])
