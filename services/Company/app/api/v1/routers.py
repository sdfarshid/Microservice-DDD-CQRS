from fastapi import APIRouter, Depends
from app.api.v1.endpoint import company
from shared.utilities.auth import verify_api_key

api_router = APIRouter(dependencies=[Depends(verify_api_key)])

api_router.include_router(company.router, prefix="/company", tags=["company"])
