from fastapi import APIRouter
from app.api.v1.endpoint import company

api_router = APIRouter()

api_router.include_router(company.router, prefix="/company", tags=["company"])
