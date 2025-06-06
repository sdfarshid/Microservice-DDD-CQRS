from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

from app.domain.product.aggregates.product import Product

TQuery = TypeVar('TQuery')
TResult = TypeVar('TResult')


class IQueryHandler(ABC):
    @abstractmethod
    async def get(self, query: TQuery) -> Optional[TResult]:
        pass

    @abstractmethod
    async def list(self, query: TQuery) -> List[TResult]:
        pass

    @abstractmethod
    async def get_batch_product_by_ids(self, query: TQuery) -> List[Product]:
        pass
