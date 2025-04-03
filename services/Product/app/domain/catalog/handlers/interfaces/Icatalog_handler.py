from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

from app.domain.catalog.handlers.interfaces.Icommand_handler import ICommandHandler
from app.domain.catalog.handlers.interfaces.Iquery_handler import IQueryHandler


class ICatalogHandler(ICommandHandler, IQueryHandler, ABC):
    pass
