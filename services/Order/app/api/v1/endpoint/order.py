from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.application.services.order_service import OrderService
from app.config.dependencies.services import get_order_service

from app.utilities.log import handle_exceptions
from shared.domain.order.commands.create_order import CreateOrderCommand

router = APIRouter()

ServiceDependency = Annotated[OrderService, Depends(get_order_service)]


@router.post("/add")
@handle_exceptions
async def create_order(command: CreateOrderCommand, service: ServiceDependency):
    result = await service.create_order(command)
    return {"message": "Invoice created successfully", "invoice_id": result.id}



#@router.on_event("startup")
#async def startup_event():
    #service = OrderService()
   # service.start()

