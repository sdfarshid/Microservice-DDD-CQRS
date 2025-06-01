from typing import Optional

from app.domain import (ICommandHandler, ICompanyRepository,
                        CompanyName, Address, CompanyStatus,
                        RegistrationNumber)
from app.domain.aggregates import Company
from shared import UpdateCompanyCommand, CompanyStatusEnum


class UpdateCompanyHandler(ICommandHandler[Company, Company | None]):
    def __init__(self, repository: ICompanyRepository):
        self.repository = repository

    async def handle(self, command: UpdateCompanyCommand) -> Optional[Company]:
        company = await self.repository.get_company_by_id(command.company_id)
        if not company:
            return None

        if command.name is not None:
            company.update_name(CompanyName(command.name))
        if command.address is not None:
            company.update_address(Address(value=command.address))
        if command.website is not None:
            company.update_website(command.website)
        if command.status is not None:
            company.update_status(CompanyStatus(value=CompanyStatusEnum(command.status)))
        if command.registration_number is not None:
            company.update_registration_number(RegistrationNumber(command.registration_number))

        await self.repository.save(company)
        return company
