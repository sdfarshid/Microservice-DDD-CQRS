import uuid
from sqlite3 import IntegrityError
from typing import List

from fastapi import Depends, HTTPException

from app.domain import ICommandHandler, IQueryHandler
from app.domain.aggregates import Company
from app.infrastructure.mappers.company_mapper import CompanyMapper, CompanyResponse
from app.utilities.log import DebugWaring
from shared import GetCompanyByIdQuery, UpdateCompanyCommand, ListCompaniesQuery, CreateCompanyCommand
from shared.domain.company.commands import DeleteCompanyCommand


class CompanyService:
    def __init__(self,
                 create_company_handler: ICommandHandler,
                 get_company_handler: IQueryHandler,
                 list_companies_handler: IQueryHandler,
                 update_company_handler: ICommandHandler,
                 delete_company_handler: ICommandHandler
                 ):
        self.create_company_handler = create_company_handler
        self.get_company_handler = get_company_handler
        self.list_companies_handler = list_companies_handler
        self.update_company_handler = update_company_handler
        self.delete_company_handler = delete_company_handler

    async def list_companies(self, query: ListCompaniesQuery) -> List[CompanyResponse]:
        try:
            listOfCompaniesDomainModel = await self.list_companies_handler.handle(query)
            return [CompanyMapper.to_response(company) for company in listOfCompaniesDomainModel]
        except Exception as e:
            raise e

    async def create_company(self, command: CreateCompanyCommand) -> uuid.UUID:
        try:
            command = CompanyMapper.convert_command_to_domain_model(command)
            DebugWaring(f"Company command: {command}")
            return await self.create_company_handler.handle(command)
        except IntegrityError:
            raise HTTPException(status_code=409,
                                detail="Company with this registration number already exists")
        except Exception as e:
            DebugWaring(f"Error in CreateCompanyHandler: {e}")
            raise e

    async def get_company_by_id(self, query: GetCompanyByIdQuery) -> CompanyResponse:
        companyDomainModel = await self.get_company_handler.handle(query)
        if not companyDomainModel:
            raise ValueError("Company not found")
        return CompanyMapper.to_response(companyDomainModel)

    async def update_company(self, command: UpdateCompanyCommand) -> CompanyResponse | None:
        companyDomainModel = await self.update_company_handler.handle(command)
        if companyDomainModel is None:
            raise ValueError("Company not found")
        return CompanyMapper.to_response(companyDomainModel)

    async def delete_company(self, company_id: uuid) -> bool:
        command = DeleteCompanyCommand(company_id=company_id)
        return await self.delete_company_handler.handle(command)
