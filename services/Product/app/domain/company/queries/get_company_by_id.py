from uuid import UUID
from pydantic import BaseModel


class GetCompanyByIdQuery(BaseModel):
    company_id: UUID