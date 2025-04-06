from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List
from uuid import UUID

TCommand = TypeVar('TCommand')
TQuery = TypeVar('TQuery')
TResult = TypeVar('TResult')


class IAssignCatalogHandler(ABC):
    @abstractmethod
    async def assign_product_to_catalogs(self, command: TCommand) -> TResult:
        pass

    @abstractmethod
    async def update_product_catalogs(self, command: TCommand) -> TResult:
        pass

    @abstractmethod
    async def get_product_catalogs(self, query: TQuery) -> TResult:
        pass
