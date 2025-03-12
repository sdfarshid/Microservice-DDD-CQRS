from fastapi import Depends

from app.domain.user.commands.auth.login_user import LoginUserCommand
from app.domain.user.handlers.interfaces.Iquery_handler import IQueryHandler
from app.domain.user.handlers.interfaces.Icommand_handler import ICommandHandler, T, R
from app.domain.user.handlers.user.get_user_by_email_handler import GetUserByEmailHandler
from app.domain.user.models.user import User
from app.domain.user.queries.get_user_by_email import GetUserByEmailQuery
from app.utilities.jwt_util import TokenData, create_access_token, create_refresh_token
from app.utilities.security import verify_password


class LoginHandler(ICommandHandler[LoginUserCommand, dict]):
    def __init__(self,
                 get_user_handler: IQueryHandler[GetUserByEmailQuery, User] = Depends(GetUserByEmailHandler)
                 ):
        self.get_user_handler = get_user_handler

    async def handle(self, command: LoginUserCommand) -> dict:
        query = GetUserByEmailQuery(command.email)
        user = await self.get_user_handler.handle(query)

        if not user or not verify_password(plain_password=command.password.value,
                                           hashed_password=user.password):
            raise ValueError("Invalid credentials")

        user_data = TokenData(
            email=str(user.email.value),
            user_id=str(user.id),
            roles=["user"],
            permissions=["read", "write"]
        )
        access_token = create_access_token(user_data)
        refresh_token = create_refresh_token(user_data)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }