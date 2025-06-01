from app.domain import IQueryHandler, ICompanyRepository
from app.domain.aggregates import Company
from shared import GetCompanyByIdQuery


class GetCompanyHandler(IQueryHandler[GetCompanyByIdQuery, Company]):
    def __init__(self, repository: ICompanyRepository):
        self.company_repository = repository

    async def handle(self, query: GetCompanyByIdQuery) -> Company | None:
        company = await self.company_repository.get_company_by_id(query.company_id)
        if not company:
            return None
        return company
