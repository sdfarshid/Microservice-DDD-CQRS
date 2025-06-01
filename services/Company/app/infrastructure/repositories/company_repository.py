from typing import Sequence, Optional
from uuid import UUID
from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.aggregates import Company
from app.infrastructure.database import CompanyDBModel
from app.infrastructure.mappers import CompanyMapper
from app.domain.interfaces.Icompany_repository import ICompanyRepository
from app.utilities.log import DebugError
from shared.mixins import PaginationParams


def _to_db_model(company: Company) -> CompanyDBModel:
    """Convert domain entity to database model"""
    return CompanyMapper.to_orm(company)


def _to_domain(db_model: CompanyDBModel) -> Company:
    """Convert database model to domain entity"""
    return CompanyMapper.to_domain(db_model)


class CompanyRepository(ICompanyRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, company: Company) -> Company:
        try:
            db_company = _to_db_model(company)
            merged_company = await self.db.merge(db_company)
            await self.db.commit()
            await self.db.refresh(merged_company)
            return _to_domain(merged_company)
        except IntegrityError as e:
            await self.db.rollback()
            DebugError(f"Integrity error in save: {e}")
            raise ValueError(f"Failed to save company: {str(e)}")
        except Exception as e:
            await self.db.rollback()
            DebugError(f"Unexpected error in save: {e}")
            raise

    async def add_company(self, company: Company) -> Company:
        try:
            db_company = _to_db_model(company)
            self.db.add(db_company)
            await self.db.commit()
            await self.db.refresh(db_company)
            return _to_domain(db_company)
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_company_by_id(self, company_id: UUID) -> Optional[Company]:
        result = await self.db.execute(
            select(CompanyDBModel)
            .where(CompanyDBModel.id == company_id)
        )
        db_company = result.scalars().one_or_none()
        if not db_company:
            return None
        return _to_domain(db_company)

    async def list_companies(self, pagination: PaginationParams) -> Sequence[Company]:
        try:
            result = await self.db.execute(
                select(CompanyDBModel).offset(pagination.offset).limit(pagination.limit)
            )
            db_companies = result.scalars().all()
            return [_to_domain(company) for company in db_companies]
        except Exception as e:
            raise e

    async def update_company(self, company_id: UUID, updated_data: dict) -> Optional[Company]:
        try:
            result = await self.db.execute(
                update(CompanyDBModel)
                .where(CompanyDBModel.id == company_id)
                .values(**updated_data)
                .returning(CompanyDBModel)
            )
            await self.db.commit()
            db_company = result.scalars().one_or_none()
            return _to_domain(db_company)
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

    async def find_by_registration_number(self, registration_number: str) -> Optional[Company]:
        result = await self.db.execute(
            select(CompanyDBModel).where(CompanyDBModel.registration_number == registration_number)
        )
        db_company = result.scalars().first()
        if not db_company:
            return None
        return _to_domain(db_company)
