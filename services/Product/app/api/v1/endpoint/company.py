from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from app.domain.company.commands.create_company import CreateCompanyCommand
from app.domain.company.services.company_service import CompanyService

router = APIRouter()


ProductServiceDependency = Annotated[CompanyService, Depends(CompanyService)]

@router.post("/register")
async def register(command: CreateCompanyCommand, service: ProductServiceDependency):
    try:
        service.create_company(command)
        return {"message": "Company created successfully"}
    except Exception as error:
        raise HTTPException(status_code=500, detail="Internal Server Error")