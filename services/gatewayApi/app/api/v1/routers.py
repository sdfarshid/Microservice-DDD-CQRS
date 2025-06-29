from fastapi import APIRouter

from app.api.v1.endpoints import product, company , user, auth

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(product.router, prefix="/product", tags=["product"])
api_router.include_router(company.router, prefix="/company", tags=["company"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
