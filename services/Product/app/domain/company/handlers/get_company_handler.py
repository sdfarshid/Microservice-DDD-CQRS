from fastapi import Depends

from app.domain.company.handlers.interfaces.Iquery_handler import IQueryHandler, T, R
from app.domain.company.models.company import Company
from app.domain.company.queries.get_company_by_id import GetCompanyByIdQuery
from app.infrastructure.mappers.company_mapper import CompanyMapper
from app.infrastructure.repositories.company_repository import CompanyRepository
from app.infrastructure.repositories.interface.Icompany_repository import ICompanyRepository


class GetCompanyHandler(IQueryHandler[GetCompanyByIdQuery, Company]):
    def __init__(self, company_repository: ICompanyRepository = Depends(CompanyRepository)):
        self.company_repository = company_repository

    async def handle(self, query: GetCompanyByIdQuery) -> R:
        company_db = await self.company_repository.get_company_by_id(query.company_id)
        print(company_db)
        if not company_db:
            return None
        return CompanyMapper.to_domain(company_db)