from fastapi import Depends

from app.domain.user.handlers.interfaces.Icommand_handler import IQueryHandler, T, R
from app.domain.user.models.user import User
from app.domain.user.queries.list_users_query import ListUsersQuery
from app.infrastructure.repositories.Interfaces.Iuser_interface import IUserRepository
from app.infrastructure.repositories.user_repository import UserRepository


class list_user_handler(IQueryHandler[ListUsersQuery, User]):
    def __init__(self, user_repository: IUserRepository = Depends(UserRepository)):
        self.user_repository = user_repository

    async def handle(self, query: ListUsersQuery) -> list[User]:
        return await self.user_repository.get_all_users(query.pagination)