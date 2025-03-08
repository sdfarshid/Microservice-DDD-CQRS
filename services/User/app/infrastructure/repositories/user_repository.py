from typing import List
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.mixins.pagination import PaginationParams
from app.domain.user.models.user import User
from app.infrastructure.database.models.user import UserDBModel
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.Interfaces.Iuser_interface import IUserRepository


class UserRepository(IUserRepository):

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all_users(self, pagination: PaginationParams) -> List[UserDBModel]:
        users: List[UserDBModel] = (
            await self.db.execute(select(UserDBModel).limit(pagination.limit).offset(pagination.offset))
        ).scalars().all()
        return users

    async def get_user_by_id(self, user_id: UUID) -> User:
        pass

    async def add(self, user: UserDBModel) -> UserDBModel:
        self.db.add(user)
        await self.db.commit()
        return user

    async def get_user_by_email(self, email: str) -> UserDBModel:
        result = await self.db.execute(select(UserDBModel).where(UserDBModel.email == email).where(UserDBModel.is_active))
        return result.scalars().first()
