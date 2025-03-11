from abc import ABC, abstractmethod
from uuid import UUID

from app.infrastructure.database.models.company import CompanyDBModel


class ICompanyRepository(ABC):

    @abstractmethod
    async def add_company(self, company: CompanyDBModel) -> CompanyDBModel:
        pass

    @abstractmethod
    async def get_company_by_id(self, company_id: UUID) -> CompanyDBModel:
        pass
