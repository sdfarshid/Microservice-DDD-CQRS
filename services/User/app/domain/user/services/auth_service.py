from fastapi import Depends


from app.domain.user.handlers.auth.login_handler import LoginHandler
from app.domain.user.handlers.auth.refresh_handler import RefreshHandler
from app.domain.user.handlers.interfaces.Icommand_handler import ICommandHandler
from app.domain.user.value_objects.Email import Email
from app.domain.user.value_objects.Password import Password
from shared.domain.user.commands import LoginUserCommand, RefreshTokenCommand


class AuthService:
    def __init__(self,
                 login_handler: ICommandHandler[LoginUserCommand, dict] = Depends(LoginHandler),
                 refresh_handler: ICommandHandler[RefreshTokenCommand, dict] = Depends(RefreshHandler)
                 ):
        self.refresh_handler = refresh_handler
        self.login_handler = login_handler

    async def login(self, email: Email, password: Password) -> dict:
        command = LoginUserCommand(email.value, password.value)
        return await self.login_handler.handle(command)

    async def refresh(self, refresh_token: str) -> dict:
        command = RefreshTokenCommand(refresh_token)
        return await self.refresh_handler.handle(command)
