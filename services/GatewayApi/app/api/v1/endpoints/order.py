from typing import Annotated, List, Optional
from uuid import UUID
from fastapi import APIRouter, Request, Depends, HTTPException, Query

from app.config.config import settings
from app.utilities.log import DebugError, DebugWaring
from app.utilities.helper import handle_exceptions, call_api

from shared.domain.order.commands.create_order import CreateOrderCommand
from shared.domain.order.queries import OrderResponse

router = APIRouter(tags=["order"])
ORDER_BASE_URL = settings.get_service_url("order")


@router.post("/")
@handle_exceptions
async def create_order(command: CreateOrderCommand):
    return await call_api(method="POST", endpoint=f"{ORDER_BASE_URL}/add", json_data=command.model_dump())
