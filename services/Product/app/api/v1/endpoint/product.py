from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter, Request, Depends, HTTPException, Query

from app.domain.product.commands.create_product import CreateProductCommand
from app.domain.product.commands.delete_product import DeleteProductCommand
from app.domain.product.commands.update_product import UpdateProductCommand
from app.domain.product.mixins.pagination import PaginationParams, get_pagination_params
from app.domain.product.aggregates.product import Product
from app.domain.product.queries.get_product_by_id import GetProductByIdQuery
from app.domain.product.queries.list_products import ListProductsQuery
from app.domain.product.services.product_service import ProductService
from app.infrastructure.mappers.product_mapper import ProductResponse

from app.domain.product.commands.reserve_product import ReserveProductCommand
from app.utilities.log import DebugError, DebugWaring

router = APIRouter()

ProductServiceDependency = Annotated[ProductService, Depends(ProductService)]


@router.post("")
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


@router.get("", response_model=List[ProductResponse])
async def list_products(service: ProductServiceDependency,
                        pagination: PaginationParams = Depends(get_pagination_params),
                        company_id: Optional[UUID] = Query(None, description="ID of the company to filter products")
                        ):
    try:
        query = ListProductsQuery(pagination=pagination, company_id=company_id)
        return await service.list_products(query)
    except ValueError as value_error:
        raise HTTPException(status_code=404, detail=str(value_error))
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        DebugError(f"Error update product : {error}")
        raise HTTPException(status_code=505, detail=str(error))


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: UUID, service: ProductServiceDependency):
    try:
        query = GetProductByIdQuery(product_id=product_id)
        product = await service.get_product(query)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except ValueError as value_error:
        raise HTTPException(status_code=404, detail=str(value_error))
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        DebugError(f"Error update product : {error}")
        raise HTTPException(status_code=505, detail=str(error))


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: UUID, command: UpdateProductCommand, service: ProductServiceDependency):
    try:
        command.product_id = product_id
        updated_product = await service.update_product(command)
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return updated_product
    except ValueError as value_error:
        raise HTTPException(status_code=404, detail=str(value_error))
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        DebugError(f"Error update product : {error}")
        raise HTTPException(status_code=505, detail=str(error))


@router.delete("/{product_id}")
async def delete_product(product_id: UUID, service: ProductServiceDependency):
    try:
        command = DeleteProductCommand(product_id=product_id)
        success = await service.delete_product(command)
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product deleted successfully"}
    except ValueError as value_error:
        raise HTTPException(status_code=404, detail=str(value_error))
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        DebugError(f"Error update product : {error}")
        raise HTTPException(status_code=505, detail=str(error))


@router.post("/reserve")
async def reserve_product(command: ReserveProductCommand, service: ProductServiceDependency):
    try:
        result = await service.reserve_products(command)
        return result
    except ValueError as value_error:
        raise HTTPException(status_code=400, detail=str(value_error))
    except Exception as error:
        DebugError(f"Error reserving products: {error}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

