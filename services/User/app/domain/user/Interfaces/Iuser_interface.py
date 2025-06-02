from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from pydantic import EmailStr

from app.domain import User
from shared.mixins import PaginationParams


class IUserRepository(ABC):
    @abstractmethod
    async def get_all_users(self, pagination: PaginationParams) -> List[User] | None:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: EmailStr) -> User:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> User:
        pass

    @abstractmethod
    async def add(self, user: User) -> User:
        pass
