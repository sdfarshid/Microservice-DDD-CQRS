from fastapi import Depends

from app.domain import User, IUserRepository
from app.domain.user.handlers.interfaces.Iquery_handler import IQueryHandler
from app.infrastructure.repositories.user_repository import UserRepository
from shared.domain.user import GetUserByEmailQuery


class GetUserByEmailHandler(IQueryHandler[GetUserByEmailQuery, User]):
    def __init__(self, user_repository: IUserRepository = Depends(UserRepository)):
        self.user_repository = user_repository

    async def handle(self, query: GetUserByEmailQuery) -> User:
        user = await self.user_repository.get_user_by_email(query.email)
        if not user:
            raise ValueError("User not found")
        return user
