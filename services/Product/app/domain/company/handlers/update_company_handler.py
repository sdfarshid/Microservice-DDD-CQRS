from typing import Tuple
from uuid import UUID

from fastapi import Depends

from app.domain.company.commands.update_company import UpdateCompanyCommand
from app.domain.company.handlers.interfaces.Icommand_handler import ICommandHandler, T, R
from app.domain.company.models.company import Company
from app.infrastructure.mappers.company_mapper import CompanyMapper
from app.infrastructure.repositories.company_repository import CompanyRepository
from app.infrastructure.repositories.interface.Icompany_repository import ICompanyRepository


class UpdateCompanyHandler(ICommandHandler[Tuple[UUID, dict], [Company, None]]):
    def __init__(self, company_repository: ICompanyRepository = Depends(CompanyRepository)):
        self.company_repository = company_repository

    async def handle(self, command: Tuple[UUID, dict]) -> [Company, None]:
        company_id, updated_data = command
        return await self.company_repository.update_company(company_id, updated_data)


