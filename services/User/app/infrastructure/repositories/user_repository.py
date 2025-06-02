from typing import List
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain import IUserRepository
from app.domain.user.models.user import User
from app.infrastructure.database.models.user import UserDBModel
from app.infrastructure.database.session import get_db
from app.infrastructure.mappers.user_mapper import UserMapper
from shared.mixins import PaginationParams


class UserRepository(IUserRepository):

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all_users(self, pagination: PaginationParams) -> List[User] | None:
        try:
            result = await self.db.execute(
                select(UserDBModel).offset(pagination.offset).limit(pagination.limit)
            )
            db_users = result.scalars().all()
            if not db_users:
                return None
            return [UserMapper.to_domain(user) for user in db_users]
        except Exception as e:
            raise e

    async def get_user_by_id(self, user_id: UUID) -> User:
        pass

    async def add(self, user: User) -> User:
        try:
            db_user = UserMapper.to_orm(user)
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
            return UserMapper.to_domain(db_user)
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(UserDBModel)
                                       .where(UserDBModel.email == email)
                                       .where(UserDBModel.is_active)
                                       )
        user_db = result.scalars().first()
        if not user_db:
            return None
        return UserMapper.to_domain(user_db)
