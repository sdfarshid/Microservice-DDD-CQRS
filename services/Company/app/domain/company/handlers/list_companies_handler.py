from typing import List

from fastapi import Depends

from app.domain.company.handlers.interfaces.Iquery_handler import IQueryHandler
from app.domain.company.models.company import Company
from app.domain.company.queries.list_companies import ListCompaniesQuery
from app.infrastructure.mappers.company_mapper import CompanyMapper
from app.infrastructure.repositories.company.company_repository import CompanyRepository


class ListCompaniesHandler(IQueryHandler[ListCompaniesQuery, List[Company]]):
    def __init__(self, company_repository: CompanyRepository = Depends(CompanyRepository)):
        self.company_repository = company_repository

    async def handle(self, query: ListCompaniesQuery) -> List[Company]:
        companies_db = await self.company_repository.list_companies(query.pagination)
        return [CompanyMapper.to_domain(company) for company in companies_db]
