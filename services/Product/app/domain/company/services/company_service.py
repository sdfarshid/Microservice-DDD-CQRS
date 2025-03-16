import uuid
from sqlite3 import IntegrityError

from fastapi import Depends, HTTPException

from app.domain.company.commands.create_company import CreateCompanyCommand
from app.domain.company.handlers.create_company_handler import CreateCompanyHandler
from app.domain.company.handlers.get_company_handler import GetCompanyHandler
from app.domain.company.handlers.interfaces.Icommand_handler import ICommandHandler
from app.domain.company.handlers.interfaces.Iquery_handler import IQueryHandler
from app.domain.company.queries.get_company_by_id import GetCompanyByIdQuery
from app.infrastructure.mappers.company_mapper import CompanyMapper, CompanyResponse
from app.utilities.log import logger


class CompanyService:
    def __init__(self,
                 create_company_handler: ICommandHandler = Depends(CreateCompanyHandler),
                 get_company_handler: IQueryHandler = Depends(GetCompanyHandler)
                 ):
        self.create_company_handler = create_company_handler
        self.get_company_handler = get_company_handler

    async def create_company(self, command: CreateCompanyCommand) -> uuid.UUID:
        try:
            return await self.create_company_handler.handler(CompanyMapper.from_command(command))
        except IntegrityError:
            raise HTTPException(status_code=409,
                                detail="Company with this registration number already exists")

    async def get_company_by_id(self, company_id: uuid) -> [CompanyResponse, Exception]:
        companyDomainModel = await self.get_company_handler.handler(GetCompanyByIdQuery(company_id=company_id))
        if not companyDomainModel:
            raise ValueError("Company not found")
        return CompanyMapper.to_response(companyDomainModel)
