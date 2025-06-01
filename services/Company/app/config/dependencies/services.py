from fastapi import Depends
from app.application.services.company_service import CompanyService
from app.domain import ICommandHandler, IQueryHandler
from app.config.dependencies.handlers import (
    get_create_company_handler,
    get_get_company_handler,
    get_list_companies_handler,
    get_update_company_handler,
    get_delete_company_handler
)


def get_company_service(
        create_company_handler: ICommandHandler = Depends(get_create_company_handler),
        get_company_handler: IQueryHandler = Depends(get_get_company_handler),
        list_companies_handler: IQueryHandler = Depends(get_list_companies_handler),
        update_company_handler: ICommandHandler = Depends(get_update_company_handler),
        delete_company_handler: ICommandHandler = Depends(get_delete_company_handler)
        ) -> CompanyService:
    return CompanyService(
        create_company_handler=create_company_handler,
        get_company_handler=get_company_handler,
        list_companies_handler=list_companies_handler,
        update_company_handler=update_company_handler,
        delete_company_handler=delete_company_handler
    )
