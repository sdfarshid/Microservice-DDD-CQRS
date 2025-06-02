from fastapi import Depends

from app.domain import User, IUserRepository, Email
from app.domain.user.handlers.interfaces.Icommand_handler import ICommandHandler
from app.infrastructure.repositories.user_repository import UserRepository
from app.utilities.security import generate_password_hash
from shared.domain.user import CreateUserCommand


class CreateUserHandler(ICommandHandler[CreateUserCommand, User]):
    def __init__(self, user_repository: IUserRepository = Depends(UserRepository)):
        self.user_repository = user_repository

    async def handle(self, command: CreateUserCommand) -> User:
        hashed_password = generate_password_hash(command.password)
        domain_user = User(
            email=Email(value=command.email),
            password=hashed_password,
        )
        return await self.user_repository.add(domain_user)
