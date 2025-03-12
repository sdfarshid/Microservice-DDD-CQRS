from fastapi import Depends

from app.domain.user.handlers.interfaces.Iquery_handler import IQueryHandler
from app.domain.user.models.user import User
from app.domain.user.queries.get_user_by_email import GetUserByEmailQuery
from app.infrastructure.mappers.user_mapper import UserMapper
from app.infrastructure.repositories.Interfaces.Iuser_interface import IUserRepository
from app.infrastructure.repositories.user_repository import UserRepository


class GetUserByEmailHandler(IQueryHandler[GetUserByEmailQuery, User]):
    def __init__(self, user_repository: IUserRepository = Depends(UserRepository)):
        self.user_repository = user_repository

    async def handle(self, query: GetUserByEmailQuery) -> User:
        user_db = await self.user_repository.get_user_by_email(query.email.value)
        if not user_db:
            raise ValueError("User not found")
        return UserMapper.to_domain(user_db)