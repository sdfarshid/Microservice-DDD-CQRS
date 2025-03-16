from http.client import HTTPException
from uuid import UUID

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from app.domain.company.handlers.interfaces.Icommand_handler import ICommandHandler, T, R
from app.domain.company.models.company import Company
from app.infrastructure.mappers.company_mapper import CompanyMapper
from app.infrastructure.repositories.company_repository import CompanyRepository
from app.infrastructure.repositories.interface.Icompany_repository import ICompanyRepository


class CreateCompanyHandler(ICommandHandler[Company, UUID]):
    def __init__(self, company_repository: ICompanyRepository = Depends(CompanyRepository)
                 ):
        self.company_repository = company_repository

    async def handler(self, companyDomainModel: Company) -> UUID:
        try:
            companyDBModel = CompanyMapper.to_orm(companyDomainModel)

            existing_company = await self.company_repository.get_by_registration_number(
                companyDBModel.registration_number)
            if existing_company:
                raise ValueError(f"Company with this registration number already exists - {existing_company.id}")
            newCompanyDBModel = await self.company_repository.add_company(companyDBModel)
            return newCompanyDBModel.id
        except IntegrityError as e:
            raise e
