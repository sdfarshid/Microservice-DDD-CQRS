from abc import abstractmethod, ABC
from typing import Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class IQueryHandler(ABC, Generic[T, R]):
    @abstractmethod
    async def handle(self, query: T) -> R:
        pass
