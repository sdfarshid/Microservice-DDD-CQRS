from abc import abstractmethod, ABC
from typing import TypeVar, Generic

T = TypeVar("T")
R = TypeVar("R")


class ICommandHandler(ABC, Generic[T, R]):

    @abstractmethod
    async def handler(self, command: T) -> R:
        pass
