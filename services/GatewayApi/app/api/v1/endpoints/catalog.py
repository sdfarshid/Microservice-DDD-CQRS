from typing import Annotated, List, Optional
from uuid import UUID
from fastapi import APIRouter, Request, Depends, HTTPException, Query

from app.config.config import settings
from app.utilities.log import DebugError, DebugWaring
from app.utilities.helper import handle_exceptions, call_api

from shared.domain.catalog.commands.update_catalog import UpdateCatalogRequest
from shared.mixins import PaginationParams, get_pagination_params
from shared.domain.catalog.queries.catalog_response import CatalogResponse
from shared.domain.catalog.commands.create_catalog import CreateCatalogCommand

router = APIRouter(tags=["catalog"])

BASE_URR_ENDPOINT = settings.get_service_url("catalog")


@router.get("/", response_model=List[CatalogResponse])
@handle_exceptions
async def list_catalogs(pagination: PaginationParams = Depends(get_pagination_params)):
    return await call_api(
        method="GET",
        endpoint=f"{BASE_URR_ENDPOINT}",
        params=pagination.model_dump()
    )


@router.get("/{catalog_id}", response_model=CatalogResponse)
@handle_exceptions
async def get_catalog(catalog_id: UUID):
    return await call_api(method="GET", endpoint=f"{BASE_URR_ENDPOINT}/{catalog_id}")


@router.post("/", response_model=CatalogResponse)
@handle_exceptions
async def create_catalog(command: CreateCatalogCommand):
    return await call_api(method="POST", endpoint=f"{BASE_URR_ENDPOINT}", json_data=command.model_dump())





@router.put("/{catalog_id}", response_model=CatalogResponse)
@handle_exceptions
async def update_catalog(catalog_id: UUID, command: UpdateCatalogRequest):
    return await call_api(method="PUT", endpoint=f"{BASE_URR_ENDPOINT}/{catalog_id}", json_data=command.model_dump())


@router.delete("/{catalog_id}")
@handle_exceptions
async def delete_catalog(catalog_id: UUID):
    return await call_api(method="DELETE", endpoint=f"{BASE_URR_ENDPOINT}/{catalog_id}")

