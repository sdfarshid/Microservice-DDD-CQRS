import uuid

from app.infrastructure.database.session import Base
from sqlalchemy import Column, String, DateTime, UUID, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class CatalogProductDBModel(Base):
    __tablename__ = 'catalog_products'
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    catalog_id = Column(PG_UUID(as_uuid=True), ForeignKey('catalogs.id'), nullable=False, index=True)
    product_id = Column(PG_UUID(as_uuid=True), ForeignKey('products.id'), nullable=False, index=True)