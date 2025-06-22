from typing import Annotated, List, Optional
from uuid import UUID
from fastapi import APIRouter, Request, Depends, HTTPException, Query

from app.config.config import settings
from app.utilities.log import DebugError, DebugWaring
from app.utilities.helper import handle_exceptions, call_api

from shared.domain.catalog.commands.update_product_catalogs import UpdateProductCatalogsCommand
from shared.domain.catalog.commands.assign_product_to_catalogs import AssignProductToCatalogsCommand

router = APIRouter()

BASE_URR_ENDPOINT = settings.get_service_url("product_catalog")

@router.post("")
@handle_exceptions
async def add_product_to_catalog(command: AssignProductToCatalogsCommand):
    return await call_api(method="POST", endpoint=f"{BASE_URR_ENDPOINT}", json_data=command.model_dump(mode='json'))




@router.get("/{product_id}")
@handle_exceptions
async def get_product_catalogs(product_id: UUID):
    return await call_api(method="GET", endpoint=f"{BASE_URR_ENDPOINT}/{product_id}")



@router.put("", response_model=dict)
@handle_exceptions
async def update_product_catalogs(command: UpdateProductCatalogsCommand):
    return await call_api(method="PUT", endpoint=f"{BASE_URR_ENDPOINT}", json_data=command.model_dump(mode='json'))

