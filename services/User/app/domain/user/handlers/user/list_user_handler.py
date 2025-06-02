from fastapi import Depends

from app.domain import IUserRepository, User
from app.domain.user.handlers.interfaces.Iquery_handler import IQueryHandler
from app.infrastructure.repositories.user_repository import UserRepository
from shared.domain.user import ListUsersQuery


class list_user_handler(IQueryHandler[ListUsersQuery, User]):
    def __init__(self, user_repository: IUserRepository = Depends(UserRepository)):
        self.user_repository = user_repository

    async def handle(self, query: ListUsersQuery) -> list[User]:
        return await self.user_repository.get_all_users(query.pagination)
