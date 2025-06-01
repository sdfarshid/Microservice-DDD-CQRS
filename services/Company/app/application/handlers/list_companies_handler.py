from typing import List

from app.domain import IQueryHandler, ICompanyRepository
from app.domain.aggregates import Company
from app.utilities.log import DebugError
from shared import ListCompaniesQuery


class ListCompaniesHandler(IQueryHandler[ListCompaniesQuery, List[Company]]):
    def __init__(self, repository: ICompanyRepository):
        self.company_repository = repository

    async def handle(self, query: ListCompaniesQuery) -> List[Company]:
        try:
            return await self.company_repository.list_companies(query.pagination)
        except Exception as e:
            DebugError(f"Error in ListCompaniesHandler: {e}")
            raise e
