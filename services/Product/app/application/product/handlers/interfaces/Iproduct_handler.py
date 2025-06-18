from abc import ABC, abstractmethod

from app.application.product.handlers.interfaces.Icommand_handler import ICommandHandler
from app.application.product.handlers.interfaces.Iquery_handler import IQueryHandler


class IProductHandler(ICommandHandler, IQueryHandler, ABC):
    pass
