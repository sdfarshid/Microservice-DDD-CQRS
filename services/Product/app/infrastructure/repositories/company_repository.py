from typing import List
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.mixins.pagination import PaginationParams
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

    async def get_company_by_id(self, company_id: UUID) -> [CompanyDBModel, None]:
        result = await self.db.execute(
            select(CompanyDBModel)
            .where(CompanyDBModel.id == company_id)
        )
        return result.scalars().one_or_none()

    async def list_companies(self, pagination: PaginationParams) -> List[CompanyDBModel]:
        result = await self.db.execute(
            select(CompanyDBModel).offset(pagination.offset).limit(pagination.limit)
        )
        return result.scalars().all()

    async def update_company(self, company_id: UUID, updated_data: dict) -> [CompanyDBModel, None]:
        try:
            result = await self.db.execute(
                update(CompanyDBModel)
                .where(CompanyDBModel.id == company_id)
                .values(**updated_data)
                .returning(CompanyDBModel)
            )
            await self.db.commit()
            return result.scalars().one_or_none()
        except Exception as e:
            await self.db.rollback()
            raise e

    async def delete_company(self, company_id: UUID) -> bool:
        try:
            result = await self.db.execute(
                delete(CompanyDBModel).where(CompanyDBModel.id == company_id)
            )
            await self.db.commit()
            return result.rowcount > 0
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_by_registration_number(self, registration_number: str) -> [CompanyDBModel , None]:
        result = await self.db.execute(
            select(CompanyDBModel).where(CompanyDBModel.registration_number == registration_number)
        )
        return result.scalars().first()


