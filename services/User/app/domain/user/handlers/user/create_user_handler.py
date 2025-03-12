from fastapi import Depends

from app.domain.user.commands.user.create_user import CreateUserCommand
from app.domain.user.handlers.interfaces.Icommand_handler import ICommandHandler
from app.domain.user.models.user import User
from app.infrastructure.mappers.user_mapper import UserMapper
from app.infrastructure.repositories.Interfaces.Iuser_interface import IUserRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.utilities.security import  generate_password_hash


class CreateUserHandler(ICommandHandler[CreateUserCommand, User]):
    def __init__(self, user_repository: IUserRepository = Depends(UserRepository)):
        self.user_repository = user_repository

    async def handle(self, command: CreateUserCommand) -> User:
        hashed_password = generate_password_hash(command.password.value)
        domain_user = User(
            email=command.email,
            password=hashed_password,
        )
        orm_user = UserMapper.to_orm(domain_user)
        await self.user_repository.add(orm_user)
        return orm_user
