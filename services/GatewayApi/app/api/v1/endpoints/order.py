from fastapi import APIRouter

from app.config.config import settings
from app.utilities.log import DebugError, DebugWaring
from app.utilities.helper import handle_exceptions, call_api

from shared.domain.order.commands.create_order import CreateOrderCommand

router = APIRouter(tags=["order"])
BASE_URR_ENDPOINT = settings.get_service_url("order")


@router.post("")
@handle_exceptions
async def create_order(command: CreateOrderCommand):
    return await call_api(method="POST", endpoint=f"{BASE_URR_ENDPOINT}/add", json_data=command.model_dump(mode="json"))
