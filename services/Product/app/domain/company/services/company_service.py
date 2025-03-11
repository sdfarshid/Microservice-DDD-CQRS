from fastapi import Depends


class CompanyService:
    def __int__(self,
                create_company_handler: ICommandHandler = Depends(CreateCompanyHandler)
                ):
        pass