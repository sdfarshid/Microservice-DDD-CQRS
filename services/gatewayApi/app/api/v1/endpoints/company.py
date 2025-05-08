from typing import Annotated, List, Optional
from uuid import UUID
from fastapi import APIRouter, Request, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from app.config.config import settings
from app.utilities.log import DebugError, DebugWaring
from app.utilities.helper import handle_exceptions, call_api

from shared.domain.company.commands.create_company import CreateCompanyCommand
from shared.domain.company.commands.update_company import UpdateCompanyCommand
from shared.mixins.pagination import PaginationParams, get_pagination_params

router = APIRouter(tags=["company"])


COMPANY_BASE_URL = settings.get_service_url("company")


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



@router.get("/{company_id}")
@handle_exceptions
async def get_company(company_id: UUID):
    return await call_api(method="GET", endpoint=f"{COMPANY_BASE_URL}/{company_id}")


@router.patch("/{company_id}")
@handle_exceptions
async def update_company(company_id: UUID, update_data: UpdateCompanyCommand):
    return await call_api(
        method="PATCH",
        endpoint=f"{COMPANY_BASE_URL}/{company_id}",
        json_data=update_data.model_dump()
    )


@router.delete("/{company_id}")
@handle_exceptions
async def delete_company(company_id: UUID):
    response = await call_api(method="DELETE", endpoint=f"{COMPANY_BASE_URL}/{company_id}")
    return response





