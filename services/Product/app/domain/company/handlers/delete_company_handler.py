from fastapi import Depends

from app.domain.company.commands.delete_company import DeleteCompanyCommand
from app.domain.company.handlers.interfaces.Icommand_handler import ICommandHandler
from app.infrastructure.repositories.company_repository import CompanyRepository


class DeleteCompanyHandler(ICommandHandler[DeleteCompanyCommand, bool]):
    def __init__(self, company_repository: CompanyRepository = Depends(CompanyRepository)):
        self.company_repository = company_repository

    async def handle(self, command: DeleteCompanyCommand) -> bool:
        return await self.company_repository.delete_company(command.company_id)

