from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.handlers.create_company_handler import CreateCompanyHandler
from app.application.handlers.get_company_handler import GetCompanyHandler
from app.application.handlers.list_companies_handler import ListCompaniesHandler
from app.application.handlers.update_company_handler import UpdateCompanyHandler
from app.application.handlers.delete_company_handler import DeleteCompanyHandler
from app.domain import ICommandHandler, IQueryHandler
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.company_repository import CompanyRepository
from app.domain.interfaces.Icompany_repository import ICompanyRepository


def get_company_repository(db: AsyncSession = Depends(get_db)) -> ICompanyRepository:
    return CompanyRepository(db=db)


def get_create_company_handler(
        repository: ICompanyRepository = Depends(get_company_repository)
) -> ICommandHandler:
    return CreateCompanyHandler(repository=repository)


def get_get_company_handler(
        repository: ICompanyRepository = Depends(get_company_repository)
) -> IQueryHandler:
    return GetCompanyHandler(repository=repository)


def get_list_companies_handler(
        repository: ICompanyRepository = Depends(get_company_repository)
) -> IQueryHandler:
    return ListCompaniesHandler(repository=repository)


def get_update_company_handler(
        repository: ICompanyRepository = Depends(get_company_repository)
) -> ICommandHandler:
    return UpdateCompanyHandler(repository=repository)


def get_delete_company_handler(
        repository: ICompanyRepository = Depends(get_company_repository)
) -> ICommandHandler:
    return DeleteCompanyHandler(repository=repository)
