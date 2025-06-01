from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.domain.aggregates import Company
from shared.mixins import PaginationParams


class ICompanyRepository(ABC):

    @abstractmethod
    async def save(self, company: Company) -> Company:
        pass

    @abstractmethod
    async def add_company(self, company: Company) -> Company:
        pass

    @abstractmethod
    async def list_companies(self, pagination: PaginationParams) -> List[Company]:
        pass

    @abstractmethod
    async def get_company_by_id(self, company_id: UUID) -> Company | None:
        pass

    @abstractmethod
    async def update_company(self, company_id: UUID, updated_data: dict) -> Company | None:
        pass

    @abstractmethod
    async def delete_company(self, company_id: UUID) -> bool:
        pass

    @abstractmethod
    async def find_by_registration_number(self, registration_number: str) -> Company | None:
        pass
