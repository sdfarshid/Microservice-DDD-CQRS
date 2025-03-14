from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.company import CompanyDBModel
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.interface.Icompany_repository import ICompanyRepository


class CompanyRepository(ICompanyRepository):
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def add_company(self, company: CompanyDBModel) -> CompanyDBModel:
        try:
            self.db.add(company)
            await self.db.commit()
            await self.db.refresh(company)
            return company
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_company_by_id(self, company_id: UUID) -> CompanyDBModel:
        result = await self.db.execute(select(CompanyDBModel).where(CompanyDBModel.id == company_id))
        return result.scalars().first()
