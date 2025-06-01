from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends

from app.application.services.company_service import CompanyService
from app.config.dependencies import get_company_service
from app.utilities.helper import handle_exceptions
from app.utilities.log import logger, DebugError, DebugWaring
from shared import (CreateCompanyCommand, CompanyResponse,
                    ListCompaniesQuery, UpdateCompanyCommand, GetCompanyByIdQuery)
from shared.mixins import PaginationParams, get_pagination_params

router = APIRouter()

CompanyServiceDependency = Annotated[CompanyService, Depends(get_company_service)]


@router.post("/create")
@handle_exceptions
async def create(command: CreateCompanyCommand, service: CompanyServiceDependency):
    company_id = await service.create_company(command)
    return {"message": "Company created successfully", "company_id": company_id}


@router.get("/companies", response_model=List[CompanyResponse])
@handle_exceptions
async def list_companies(service: CompanyServiceDependency,
                         pagination: PaginationParams = Depends(get_pagination_params)):
    query = ListCompaniesQuery(pagination=pagination)
    return await service.list_companies(query)


@router.get("/{company_id}", response_model=CompanyResponse)
@handle_exceptions
async def get_company(company_id: UUID, service: CompanyServiceDependency):
    return await service.get_company_by_id(GetCompanyByIdQuery(company_id=company_id))


@router.patch("/{company_id}", response_model=CompanyResponse)
@handle_exceptions
async def update_company(updateData: UpdateCompanyCommand, service: CompanyServiceDependency):
    return await service.update_company(updateData)


@router.delete("/{company_id}")
@handle_exceptions
async def delete_company(company_id: UUID, service: CompanyServiceDependency):
    success = await service.delete_company(company_id)
    if not success:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": "Company deleted successfully"}
