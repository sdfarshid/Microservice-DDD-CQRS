from app.domain.company.commands.create_company import CreateCompanyCommand
from app.domain.company.handlers.interfaces.Icommand_handler import ICommandHandler, T, R
from app.domain.company.models.company import Company


class CreateCompanyHandler(ICommandHandler[CreateCompanyCommand, Company]):
    def __init__(self):
        pass

    def handler(self, command: T) -> R:
        pass