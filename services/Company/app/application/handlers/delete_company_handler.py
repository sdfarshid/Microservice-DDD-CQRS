from app.domain import ICommandHandler, ICompanyRepository
from shared.domain.company.commands import DeleteCompanyCommand


class DeleteCompanyHandler(ICommandHandler[DeleteCompanyCommand, bool]):
    def __init__(self, repository: ICompanyRepository):
        self.company_repository = repository

    async def handle(self, command: DeleteCompanyCommand) -> bool:
        return await self.company_repository.delete_company(command.company_id)

