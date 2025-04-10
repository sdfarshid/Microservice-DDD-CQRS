from app.domain.product.handlers.interfaces.Icommand_handler import ICommandHandler
from app.domain.product.handlers.interfaces.Iquery_handler import IQueryHandler
from abc import ABC, abstractmethod


class IProductHandler(ICommandHandler, IQueryHandler, ABC):
    pass
