from fastapi import APIRouter

from app.api.v1.endpoint import product

api_router = APIRouter()

api_router.include_router(product.router, prefix="/product", tags=["product"])
