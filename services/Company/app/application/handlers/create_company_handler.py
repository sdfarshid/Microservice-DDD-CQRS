from uuid import UUID
from sqlalchemy.exc import IntegrityError
from app.domain import ICommandHandler, ICompanyRepository
from app.domain.aggregates import Company


class CreateCompanyHandler(ICommandHandler[Company, UUID]):
    def __init__(self, repository: ICompanyRepository):
        self.company_repository = repository

    async def handle(self, companyDomain: Company) -> UUID:
        try:
            existing_company = await self.company_repository.find_by_registration_number(
                companyDomain.registration_number.value)
            if existing_company:
                raise ValueError(f"Company with this registration number already exists - {existing_company.id}")
            new_company = await self.company_repository.save(companyDomain)
            return new_company.id
        except IntegrityError as e:
            raise e
