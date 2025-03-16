from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends

from app.domain.company.commands.create_company import CreateCompanyCommand
from app.domain.company.queries.get_company_by_id import GetCompanyByIdQuery
from app.domain.company.services.company_service import CompanyService
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


@router.get("/companies/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: UUID, service: ProductServiceDependency):
    try:
        return await service.get_company_by_id(company_id)
    except ValueError as value_error:
        raise HTTPException(status_code=404, detail="Company not found")
    except Exception as error:
        raise HTTPException(status_code=500, detail="Internal Server Error")

