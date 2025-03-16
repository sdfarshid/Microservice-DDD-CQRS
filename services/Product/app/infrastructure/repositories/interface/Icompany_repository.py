
from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.domain.mixins.pagination import PaginationParams
from app.infrastructure.database.models.company import CompanyDBModel


class ICompanyRepository(ABC):

    @abstractmethod
    async def add_company(self, company: CompanyDBModel) -> CompanyDBModel:
        pass

    @abstractmethod
    async def list_companies(self, pagination: PaginationParams) -> List[CompanyDBModel]:
        pass

    @abstractmethod
    async def get_company_by_id(self, company_id: UUID) -> [CompanyDBModel, None]:
        pass

    @abstractmethod
    async def update_company(self, company_id: UUID, updated_data: dict) -> [CompanyDBModel, None]:
        pass

    @abstractmethod
    async def delete_company(self, company_id: UUID) -> bool:
        pass
    @abstractmethod
    async def get_by_registration_number(self, registration_number: str) -> [CompanyDBModel, None]:
        pass
