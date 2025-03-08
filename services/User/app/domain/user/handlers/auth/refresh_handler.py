from app.domain.user.commands.auth.refresh_token import RefreshTokenCommand
from app.domain.user.handlers.interfaces.Iquery_handler import ICommandHandler
from app.utilities.jwt_util import create_access_token, create_refresh_token, verify_token, TokenData


class RefreshHandler(ICommandHandler[RefreshTokenCommand, dict]):
    def __init__(self):
        pass

    async def handle(self, command: RefreshTokenCommand) -> dict:
        #  Refresh Token
        payload = verify_token(command.refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")

        user_data = TokenData(
            email=payload["email"],
            user_id=payload["user_id"],
            roles=payload["roles"],
            permissions=payload["permissions"]
        )

        new_access_token = create_access_token(user_data)
        new_refresh_token = create_refresh_token(user_data)
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
