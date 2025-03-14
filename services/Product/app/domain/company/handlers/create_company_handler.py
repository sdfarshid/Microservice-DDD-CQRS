from fastapi import Depends

from app.domain.company.handlers.interfaces.Icommand_handler import ICommandHandler, T, R
from app.domain.company.models.company import Company
from app.infrastructure.mappers.company_mapper import CompanyMapper
from app.infrastructure.repositories.company_repository import CompanyRepository
from app.infrastructure.repositories.interface.Icompany_repository import ICompanyRepository


class CreateCompanyHandler(ICommandHandler[Company, None]):
    def __init__(self, company_repository: ICompanyRepository = Depends(CompanyRepository)
                 ):
        self.company_repository = company_repository

    async def handle(self, company: Company):
        CompanyDBModel = CompanyMapper.to_orm(company)
        await self.company_repository.add_company(CompanyDBModel)