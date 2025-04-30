from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.application.commands.create_order import CreateOrderCommand
from app.application.services.order_service import OrderService
from app.utilities.log import DebugError

router = APIRouter()

ServiceDependency = Annotated[OrderService, Depends(OrderService)]


@router.post("/add")
async def create_order(command: CreateOrderCommand, service: ServiceDependency):
    try:
        result = await service.create_order(command)
        return {"message": "Invoice created successfully", "invoice_id": result.id}
    except ValueError as value_error:
        raise HTTPException(status_code=409, detail=str(value_error))
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        DebugError(f"Error create Order : {error}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


#@router.on_event("startup")
#async def startup_event():
    #service = OrderService()
   # service.start()

