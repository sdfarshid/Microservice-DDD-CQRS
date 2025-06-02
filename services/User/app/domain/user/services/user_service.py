from uuid import UUID
from fastapi import Depends

from app.domain import Email, Password, User
from app.domain.user.handlers.interfaces.Icommand_handler import ICommandHandler
from app.domain.user.handlers.interfaces.Iquery_handler import IQueryHandler
from app.domain.user.handlers.user.create_user_handler import CreateUserHandler
from app.domain.user.handlers.user.list_user_handler import list_user_handler
from app.domain.user.models.user import UserResponse
from app.infrastructure.mappers.user_mapper import UserMapper
from shared.domain.user import ListUsersQuery, CreateUserCommand
from shared.mixins import PaginationParams


class UserService:
    def __init__(self,
                 create_user_handler: ICommandHandler = Depends(CreateUserHandler),
                 list_users_handler: IQueryHandler = Depends(list_user_handler)
                 ):
        self.create_user_handler = create_user_handler
        self.list_users_handler = list_users_handler

    async def list_users(self, pagination: PaginationParams) -> list[UserResponse]:
        all_users = await self.list_users_handler.handle(ListUsersQuery(pagination))
        if not all_users:
            return []
        return [UserMapper.to_response(user) for user in all_users]

    async def create_user(self, email: Email, password: Password) -> UserResponse:
        command = CreateUserCommand(email.value, password.value)
        user = await self.create_user_handler.handle(command)
        return UserMapper.to_response(user)

    async def get_user(self, user_id: UUID) -> User:
        # Logic to get a user
        pass
