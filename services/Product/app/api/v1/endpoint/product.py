from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter, Request, Depends, HTTPException, Query

from app.application.product.services.product_service import ProductService

from app.utilities.log import handle_exceptions, DebugError
from shared.domain.product.commands import ReserveProductCommand
from shared.domain.product.commands import CreateProductCommand
from shared.domain.product.commands.delete_product import DeleteProductCommand
from shared.domain.product.commands.update_product import UpdateProductRequest
from shared.domain.product.queries.get_product_by_id import GetProductByIdQuery
from shared.domain.product.queries.list_products import ListProductsQuery
from shared.domain.product.responsies.product_response import ProductResponse
from shared.mixins.pagination import PaginationParams, get_pagination_params

router = APIRouter()

ProductServiceDependency = Annotated[ProductService, Depends(ProductService)]


@router.post("")
@handle_exceptions
async def create_product(command: CreateProductCommand, service: ProductServiceDependency):
    result = await service.create_product(command)
    return {"message": "Product created successfully", "id": result.id}


@router.get("", response_model=List[ProductResponse])
@handle_exceptions
async def list_products(service: ProductServiceDependency,
                        pagination: PaginationParams = Depends(get_pagination_params),
                        company_id: Optional[UUID] = Query(None, description="ID of the company to filter products")
                        ):
    query = ListProductsQuery(pagination=pagination, company_id=company_id)
    return await service.list_products(query)


@router.get("/{product_id}", response_model=ProductResponse)
@handle_exceptions
async def get_product(product_id: UUID, service: ProductServiceDependency):
    product = await service.get_product(GetProductByIdQuery(product_id=product_id))
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
@handle_exceptions
async def update_product(product_id: UUID, command: UpdateProductRequest, service: ProductServiceDependency):
    command.product_id = product_id
    updated_product = await service.update_product(command)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@router.delete("/{product_id}")
@handle_exceptions
async def delete_product(product_id: UUID, service: ProductServiceDependency):
    success = await service.delete_product(DeleteProductCommand(product_id=product_id))
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}


@router.put("/release")
@handle_exceptions
async def release_reserved_products(command: ReserveProductCommand, service: ProductServiceDependency):
    DebugError(f"Error reserving products: {command.model_dump()}")
    return await service.release_reserved_products(command)


@router.post("/reserve")
@handle_exceptions
async def reserve_product(command: ReserveProductCommand, service: ProductServiceDependency):
    return await service.reserve_products(command)
