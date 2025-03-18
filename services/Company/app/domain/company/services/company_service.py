import uuid
from sqlite3 import IntegrityError
from typing import List

from fastapi import Depends, HTTPException

from app.domain.company.commands.create_company import CreateCompanyCommand
from app.domain.company.commands.delete_company import DeleteCompanyCommand
from app.domain.company.commands.update_company import UpdateCompanyCommand
from app.domain.company.handlers.create_company_handler import CreateCompanyHandler
from app.domain.company.handlers.delete_company_handler import DeleteCompanyHandler
from app.domain.company.handlers.get_company_handler import GetCompanyHandler
from app.domain.company.handlers.interfaces.Icommand_handler import ICommandHandler
from app.domain.company.handlers.interfaces.Iquery_handler import IQueryHandler
from app.domain.company.handlers.list_companies_handler import ListCompaniesHandler
from app.domain.company.handlers.update_company_handler import UpdateCompanyHandler
from app.domain.company.models.company import Company
from app.domain.company.queries.get_company_by_id import GetCompanyByIdQuery
from app.domain.company.queries.list_companies import ListCompaniesQuery
from app.infrastructure.mappers.company_mapper import CompanyMapper, CompanyResponse
from app.utilities.log import logger, DebugWaring, DebugError


class CompanyService:
    def __init__(self,
                 create_company_handler: ICommandHandler = Depends(CreateCompanyHandler),
                 get_company_handler: IQueryHandler = Depends(GetCompanyHandler),
                 list_companies_handler: IQueryHandler = Depends(ListCompaniesHandler),
                 update_company_handler: ICommandHandler = Depends(UpdateCompanyHandler),
                 delete_company_handler: ICommandHandler = Depends(DeleteCompanyHandler)
                 ):
        self.create_company_handler = create_company_handler
        self.get_company_handler = get_company_handler
        self.list_companies_handler = list_companies_handler
        self.update_company_handler = update_company_handler
        self.delete_company_handler = delete_company_handler

    async def create_company(self, command: CreateCompanyCommand) -> uuid.UUID:
        try:
            command = CompanyMapper.convert_command_to_domain_model(command)
            return await self.create_company_handler.handle(command)
        except IntegrityError:
            raise HTTPException(status_code=409,
                                detail="Company with this registration number already exists")

    async def get_company_by_id(self, company_id: uuid) -> [CompanyResponse, Exception]:
        companyDomainModel = await self.get_company_handler.handle(GetCompanyByIdQuery(company_id=company_id))
        if not companyDomainModel:
            raise ValueError("Company not found")
        return CompanyMapper.to_response(companyDomainModel)

    async def list_companies(self, query: ListCompaniesQuery) -> List[CompanyResponse]:
        listOfCompaniesDomainModel = await self.list_companies_handler.handle(query)
        return [CompanyMapper.to_response(company) for company in listOfCompaniesDomainModel]

    async def update_company(self, command: UpdateCompanyCommand) -> [Company, None]:
        query = GetCompanyByIdQuery(company_id=command.company_id)
        company = await self.get_company_handler.handle(query)
        if not company:
            raise ValueError("Company not found")

        updated_company = CompanyMapper.update_from_command(company, command)
        return await self.update_company_handler.handle((command.company_id, updated_company))

    async def delete_company(self, company_id: uuid) -> bool:
        command = DeleteCompanyCommand(company_id=company_id)
        return await self.delete_company_handler.handle(command)


