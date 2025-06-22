from typing import Annotated, List, Optional
from uuid import UUID
from functools import wraps
from fastapi import APIRouter, Depends, HTTPException, Query

from app.application.catalog.services.assign_catalog_service import AssignCatalogService
from app.utilities.log import DebugError
from shared.domain.catalog.commands.assign_product_to_catalogs import AssignProductToCatalogsCommand
from shared.domain.catalog.commands.update_product_catalogs import UpdateProductCatalogsCommand
from shared.domain.catalog.queries.get_product_catalogs import GetProductCatalogsQuery

router = APIRouter()

AssignCatalogServiceDependency = Annotated[AssignCatalogService, Depends(AssignCatalogService)]


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


@router.post("")
@handle_exceptions
async def add_product_to_catalog(command: AssignProductToCatalogsCommand, service: AssignCatalogServiceDependency):
    success = await service.add_product_to_catalog(command)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add product to catalog")
    return {"message": "Product added to catalog successfully"}


@router.put("", response_model=dict)
async def update_product_catalogs(
        command: UpdateProductCatalogsCommand,
        service: AssignCatalogServiceDependency
):
    success = await service.update_product_catalogs(command)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update product catalogs")
    return {"message": "Product catalogs updated successfully"}


@router.get("/{product_id}")
@handle_exceptions
async def get_product_catalogs(product_id: UUID, service: AssignCatalogServiceDependency):
    query = GetProductCatalogsQuery(product_id=product_id)
    return await service.get_product_catalogs(query)
