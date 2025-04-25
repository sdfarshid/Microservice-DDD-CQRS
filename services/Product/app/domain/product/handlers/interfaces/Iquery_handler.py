from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

TQuery = TypeVar('TQuery')
TResult = TypeVar('TResult')


class IQueryHandler(ABC):
    @abstractmethod
    async def get(self, query: TQuery) -> Optional[TResult]:
        pass

    @abstractmethod
    async def list(self, query: TQuery) -> List[TResult]:
        pass
