from typing import Annotated, List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query

from app.utilities.log import handle_exceptions

from app.application.catalog.services.catalog_service import CatalogService
from shared.domain.catalog.commands.delete_catalog import DeleteCatalogCommand
from shared.domain.catalog.queries.get_catalog_by_id import GetCatalogByIdQuery
from shared.domain.catalog.queries.list_catalogs import ListCatalogsQuery
from shared.mixins import PaginationParams, get_pagination_params
from shared.domain.catalog.queries.catalog_response import CatalogResponse
from shared.domain.catalog.commands.create_catalog import CreateCatalogCommand
from shared.domain.catalog.commands.update_catalog import UpdateCatalogRequest

router = APIRouter()

CatalogServiceDependency = Annotated[CatalogService, Depends(CatalogService)]


@router.post("", response_model=CatalogResponse)
@handle_exceptions
async def create_catalog(command: CreateCatalogCommand, service: CatalogServiceDependency):
    return await service.create_catalog(command)


@router.get("", response_model=List[CatalogResponse])
@handle_exceptions
async def list_catalogs(
        service: CatalogServiceDependency,
        pagination: PaginationParams = Depends(get_pagination_params),
        ):
    return await service.list_catalogs(ListCatalogsQuery(pagination=pagination))


@router.get("/{catalog_id}", response_model=CatalogResponse)
@handle_exceptions
async def get_catalog(catalog_id: UUID, service: CatalogServiceDependency):
    query = GetCatalogByIdQuery(catalog_id=catalog_id)
    return await service.get_catalog(query)


@router.put("/{catalog_id}", response_model=CatalogResponse)
@handle_exceptions
async def update_catalog(catalog_id: UUID, command: UpdateCatalogRequest, service: CatalogServiceDependency):
    updated_catalog = await service.update_catalog(catalog_id, command)
    if not updated_catalog:
        raise HTTPException(status_code=404, detail="Catalog not found")
    return updated_catalog


@router.delete("/{catalog_id}")
@handle_exceptions
async def delete_catalog(catalog_id: UUID, service: CatalogServiceDependency):
    command = DeleteCatalogCommand(catalog_id=catalog_id)
    success = await service.delete_catalog(command)
    if not success:
        raise HTTPException(status_code=404, detail="Catalog not found")
    return {"message": "Catalog deleted successfully"}
