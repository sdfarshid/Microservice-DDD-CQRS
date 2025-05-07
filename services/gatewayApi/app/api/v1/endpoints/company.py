from typing import Annotated, List, Optional
from uuid import UUID
from fastapi import APIRouter, Request, Depends, HTTPException, Query

from app.config.config import settings
from app.utilities.log import DebugError, DebugWaring

from app.utilities.helper import handle_exceptions, call_api

router = APIRouter(tags=["product"])

PRODUCT_SERVICE_URL = settings.PRODUCT_SERVICE_URL
BASE_PATH = "api/v1/product"
PRODUCT_BASE_URL = f"{PRODUCT_SERVICE_URL}{BASE_PATH}"

DebugError(f"PRODUCT_BASE_URL: {PRODUCT_BASE_URL}")


@router.get("/{product_id}")
@handle_exceptions
async def get_product(product_id: UUID):
    return await call_api(method="GET", endpoint=f"{PRODUCT_BASE_URL}/{product_id}")


@router.post("/")
@handle_exceptions
async def create_product(command: dict):
    return await call_api(method="POST", endpoint=f"{PRODUCT_BASE_URL}/", json_data=command)

@router.post("/create")
@handle_exceptions
async def create(command: CreateCompanyCommand):
    return await call_api(method="POST", endpoint=f"{COMPANY_BASE_URL}/create", json_data=command.model_dump())



@router.get("/companies")
@handle_exceptions
async def list_companies(
        pagination: PaginationParams = Depends(get_pagination_params)
):
    return await call_api(method="GET", endpoint=f"{COMPANY_BASE_URL}/companies", params=pagination.model_dump())



@router.get("/", response_model=List[dict])
@handle_exceptions
async def list_products(
        company_id: Optional[UUID] = Query(None, description="ID of the company to filter products"),
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100)
):
    params = {"page": page, "page_size": page_size}
    if company_id:
        params["company_id"] = str(company_id)
    return await call_api(method="GET", endpoint=f"{PRODUCT_BASE_URL}", params=params)


@router.put("/{product_id}")
@handle_exceptions
async def update_product(product_id: UUID, command: dict):
    return await call_api(method="PUT", endpoint=f"{PRODUCT_BASE_URL}/{product_id}", json_data=command)


@router.delete("/{product_id}")
@handle_exceptions
async def delete_product(product_id: UUID):
    return await call_api(method="DELETE", endpoint="{PRODUCT_BASE_URL}/{product_id}")
