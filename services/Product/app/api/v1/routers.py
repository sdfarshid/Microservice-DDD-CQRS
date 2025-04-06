from fastapi import APIRouter

from app.api.v1.endpoint import product, catalog, product_catalog

api_router = APIRouter()

api_router.include_router(product.router, prefix="/product", tags=["product"])
api_router.include_router(catalog.router, prefix="/catalog", tags=["catalog"])
api_router.include_router(product_catalog.router, prefix="/productCatalog", tags=["ProductCatalog"])
