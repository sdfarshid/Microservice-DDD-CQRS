from abc import ABC, abstractmethod
from typing import TypeVar

TCommand = TypeVar('TCommand')
TResult = TypeVar('TResult')


class ICommandHandler(ABC):
    @abstractmethod
    async def create(self, command: TCommand) -> TResult:
        pass

    @abstractmethod
    async def update(self, command: TCommand) -> TResult:
        pass

    @abstractmethod
    async def delete(self, command: TCommand) -> bool:
        pass

