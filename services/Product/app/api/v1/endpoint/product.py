from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Request, Depends, HTTPException

from app.domain.product.commands.create_product import CreateProductCommand
from app.domain.product.commands.update_product import UpdateProductCommand
from app.domain.product.mixins.pagination import PaginationParams, get_pagination_params
from app.domain.product.models.product import Product
from app.domain.product.queries.get_product_by_id import GetProductByIdQuery
from app.domain.product.queries.list_products import ListProductsQuery
from app.domain.product.services.product_service import ProductService
from app.utilities.log import DebugError

router = APIRouter()

ProductServiceDependency = Annotated[ProductService, Depends(ProductService)]


@router.post("/products")
async def create_product(command: CreateProductCommand, service: ProductServiceDependency):
    try:
        result = await service.create_product(command)
        return {"message": "Product created successfully", "id": result.id}
    except ValueError as value_error:
        raise HTTPException(status_code=409, detail=str(value_error))
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        DebugError(f"Error create product : {error}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: UUID, service: ProductServiceDependency):
    query = GetProductByIdQuery(product_id=product_id)
    product = await service.get_product(query)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/products", response_model=List[Product])
async def list_products(service: ProductServiceDependency,
                        pagination: PaginationParams = Depends(get_pagination_params)):
    query = ListProductsQuery(pagination=pagination)
    return await service.list_products(query)


@router.put("/{product_id}", response_model=Product)
async def update_product(product_id: UUID, command: UpdateProductCommand, service: ProductServiceDependency):
    command.product_id = product_id
    updated_product = await service.update_product(command)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@router.delete("/{product_id}")
async def delete_product(product_id: UUID, service: ProductServiceDependency):
    success = await service.delete_product(command)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
