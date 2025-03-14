from fastapi import Depends

from app.domain.company.commands.create_company import CreateCompanyCommand
from app.domain.company.handlers.create_company_handler import CreateCompanyHandler
from app.domain.company.handlers.interfaces.Icommand_handler import ICommandHandler
from app.infrastructure.mappers.company_mapper import CompanyMapper


class CompanyService:
    def __int__(self,
                create_company_handler: ICommandHandler = Depends(CreateCompanyHandler)
                ):
        self.create_company_handler = create_company_handler

    def create_company(self, command: CreateCompanyCommand):

        self.create_company_handler.handler(CompanyMapper.from_command(command))
