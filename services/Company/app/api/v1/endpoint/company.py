from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends

from app.domain.company.commands.create_company import CreateCompanyCommand
from app.domain.company.commands.delete_company import DeleteCompanyCommand
from app.domain.company.commands.update_company import UpdateCompanyCommand
from app.domain.company.queries.get_company_by_id import GetCompanyByIdQuery
from app.domain.company.queries.list_companies import ListCompaniesQuery
from app.domain.company.services.company_service import CompanyService
from app.domain.mixins.pagination import PaginationParams, get_pagination_params
from app.infrastructure.mappers.company_mapper import CompanyResponse
from app.utilities.log import logger, DebugError, DebugWaring

router = APIRouter()

ProductServiceDependency = Annotated[CompanyService, Depends(CompanyService)]


@router.post("/register")
async def register(command: CreateCompanyCommand, service: ProductServiceDependency):
    try:
        company_id = await service.create_company(command)
        return {"message": "Company created successfully", "company_id": company_id}
    except ValueError as value_error:
        raise HTTPException(status_code=409, detail=str(value_error))
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        DebugError(f"Error: {error}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/companies", response_model=List[CompanyResponse])
async def list_companies(
        service: ProductServiceDependency,
        pagination: PaginationParams = Depends(get_pagination_params)
):
    DebugWaring(pagination)
    query = ListCompaniesQuery(pagination=pagination)
    return await service.list_companies(query)




@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: UUID, service: ProductServiceDependency):
    try:
        return await service.get_company_by_id(company_id)
    except ValueError as value_error:
        raise HTTPException(status_code=404, detail="Company not found")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Internal Server Error")




@router.patch("/{company_id}", response_model=CompanyResponse)
async def get_company(updateData: UpdateCompanyCommand, service: ProductServiceDependency):
    try:
        return await service.update_company(updateData)
    except ValueError as value_error:
        raise HTTPException(status_code=404, detail="Company not found")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Internal Server Error")





@router.delete("/{company_id}")
async def delete_company(company_id: UUID, service: ProductServiceDependency):
    success = await service.delete_company(company_id)
    if not success:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": "Company deleted successfully"}



