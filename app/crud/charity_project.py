from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return project_id.scalars().first()

    async def remove(
        self,
        db_obj,
        session: AsyncSession
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def update(
        self,
        obj_in,
        db_obj,
        session: AsyncSession
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[CharityProject]:
        query = await session.execute(
            select(CharityProject)
            .where(
                CharityProject.fully_invested
            )
            .order_by(
                extract(
                    'epoch',
                    CharityProject.close_date - CharityProject.create_date
                )
            )
        )
        return query.scalars().all()


charityproject_crud = CRUDCharityProject(CharityProject)
