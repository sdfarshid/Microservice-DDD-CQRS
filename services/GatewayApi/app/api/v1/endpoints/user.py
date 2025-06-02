from fastapi import APIRouter, Depends

from app.config.config import settings
from app.utilities.helper import handle_exceptions, call_api
from shared.domain.user.commands.user.create_user import CreateUserRequest
from shared.mixins import PaginationParams, get_pagination_params

router = APIRouter(tags=["user"])
User_BASE_URL = settings.get_service_url("user")


@router.post("/create")
@handle_exceptions
async def create(command: CreateUserRequest):
    return await call_api(
        method="POST",
        endpoint=f"{User_BASE_URL}/register",
        json_data=command.model_dump()
    )


@router.get("/users")
@handle_exceptions
async def get_users(pagination: PaginationParams = Depends(get_pagination_params)):
    return await call_api(
        method="GET",
        endpoint=f"{User_BASE_URL}/users",
        params=pagination.model_dump()
    )
