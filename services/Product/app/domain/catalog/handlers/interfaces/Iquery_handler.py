from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List
from uuid import UUID

from app.domain.catalog.models.catalog import Catalog

TQuery = TypeVar('TQuery')
TResult = TypeVar('TResult')


class IQueryHandler(ABC):
    @abstractmethod
    async def get(self, query: TQuery) -> [TResult, None]:
        pass

    @abstractmethod
    async def list(self, query: TQuery) -> List[TResult]:
        pass

    @abstractmethod
    async def find_by_name(self,  query: TQuery) -> [TResult, None]:
        pass

    @abstractmethod
    async def get_by_ids(self,  query: TQuery) -> [TResult, None]:
        pass

