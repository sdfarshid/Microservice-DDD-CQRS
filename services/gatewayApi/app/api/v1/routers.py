from fastapi import APIRouter

from app.api.v1.endpoints import product, company

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(product.router, prefix="/product", tags=["product"])
api_router.include_router(company.router, prefix="/company", tags=["company"])
