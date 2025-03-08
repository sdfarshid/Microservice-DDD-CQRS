from uuid import UUID
from fastapi import Depends

from app.domain.mixins.pagination import PaginationParams
from app.domain.user.commands.user.create_user import CreateUserCommand
from app.domain.user.handlers.user.create_user_handler import CreateUserHandler
from app.domain.user.handlers.interfaces.Icommand_handler import IQueryHandler
from app.domain.user.handlers.interfaces.Iquery_handler import ICommandHandler
from app.domain.user.handlers.user.list_user_handler import list_user_handler
from app.domain.user.models.user import User, UserResponse
from app.domain.user.queries.list_users_query import ListUsersQuery
from app.domain.user.value_objects.Email import Email
from app.domain.user.value_objects.Password import Password


class UserService:
    def __init__(self,
                 create_user_handler: ICommandHandler = Depends(CreateUserHandler),
                 list_users_handler: IQueryHandler = Depends(list_user_handler)
                 ):
        self.create_user_handler = create_user_handler
        self.list_users_handler = list_users_handler

    async def list_users(self, pagination: PaginationParams) -> list[UserResponse]:
        all_users = await self.list_users_handler.handle(ListUsersQuery(pagination))
        return [UserResponse.model_validate(user) for user in all_users]

    async def create_user(self, email: Email, password: Password) -> UserResponse:
        command = CreateUserCommand(email, password)
        orm_user = await self.create_user_handler.handle(command)
        return UserResponse.model_validate(orm_user)

    async def get_user(self, user_id: UUID) -> User:
        # Logic to get a user
        pass
