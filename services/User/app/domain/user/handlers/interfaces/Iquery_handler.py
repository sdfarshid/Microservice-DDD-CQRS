from abc import abstractmethod, ABC
from typing import Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class ICommandHandler(ABC, Generic[T, R]):
    @abstractmethod
    async def handle(self, command: T) -> R:
        pass
