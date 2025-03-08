from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.domain.mixins.pagination import PaginationParams
from app.infrastructure.database.models.user import UserDBModel


class IUserRepository(ABC):
    @abstractmethod
    async def get_all_users(self, pagination: PaginationParams) -> List[UserDBModel]:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserDBModel:
        pass
    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> UserDBModel:
        pass

    @abstractmethod
    async def add(self, user: UserDBModel) -> UserDBModel:
        pass
