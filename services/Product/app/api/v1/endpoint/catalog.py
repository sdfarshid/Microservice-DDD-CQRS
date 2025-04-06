from typing import Annotated, List, Optional
from uuid import UUID
from functools import wraps
from fastapi import APIRouter, Depends, HTTPException, Query

from app.domain.catalog.commands.create_catalog import CreateCatalogCommand
from app.domain.catalog.commands.delete_catalog import DeleteCatalogCommand
from app.domain.catalog.commands.update_catalog import UpdateCatalogCommand
from app.domain.catalog.queries.get_catalog_by_id import GetCatalogByIdQuery
from app.domain.catalog.queries.list_catalogs import ListCatalogsQuery
from app.domain.catalog.services.assign_catalog_service import AssignCatalogService
from app.domain.catalog.services.catalog_service import CatalogService
from app.domain.catalog.mixins.pagination import PaginationParams, get_pagination_params
from app.infrastructure.mappers.catalog_mapper import CatalogResponse
from app.utilities.log import DebugError

router = APIRouter()

CatalogServiceDependency = Annotated[CatalogService, Depends(CatalogService)]


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as value_error:
            raise HTTPException(status_code=404, detail=str(value_error))
        except HTTPException as http_error:
            raise http_error
        except Exception as error:
            DebugError(f"Error in {func.__name__}: {error}")
            raise HTTPException(status_code=500, detail="Internal server error")

    return wrapper


@router.post("/catalogs", response_model=CatalogResponse)
@handle_exceptions
async def create_catalog(command: CreateCatalogCommand, service: CatalogServiceDependency):
    return await service.create_catalog(command)


@router.get("/catalogs", response_model=List[CatalogResponse])
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
    catalog = await service.get_catalog(query)
    if not catalog:
        raise HTTPException(status_code=404, detail="Catalog not found")
    return catalog


@router.put("/{catalog_id}", response_model=CatalogResponse)
@handle_exceptions
async def update_catalog(catalog_id: UUID, command: UpdateCatalogCommand, service: CatalogServiceDependency):
    command.catalog_id = catalog_id
    updated_catalog = await service.update_catalog(command)
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

