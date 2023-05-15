from typing import Optional, Sequence
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.sql.base import ExecutableOption

from app.models import Petition
from app.repositories.base import BaseRepository


class PetitionFilter(BaseModel):
    title: Optional[str] = None
    user_id: Optional[UUID] = None


class PetitionRepository(BaseRepository[Petition]):
    __model__ = Petition

    async def find(
            self,
            petition_filter: PetitionFilter,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Sequence[Petition]:
        query = select(self.__model__)

        if petition_filter.title is not None:
            query = query.filter(Petition.title.contains(petition_filter.title))
        if petition_filter.user_id is not None:
            query = query.filter_by(user_id=petition_filter.user_id)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).all()

    async def find_one(
            self,
            petition_filter: PetitionFilter,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Optional[Petition]:
        query = select(self.__model__).limit(1)

        if petition_filter.title is not None:
            query = query.filter(Petition.title.contains(petition_filter.title))
        if petition_filter.user_id is not None:
            query = query.filter_by(user_id=petition_filter.user_id)
        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).first()

    async def get_count_by_filter(self, petition_filter: PetitionFilter) -> Optional[int]:
        query = select(func.count()).select_from(self.__model__)

        if petition_filter.title is not None:
            query = query.filter(Petition.title.contains(petition_filter.title))
        if petition_filter.user_id is not None:
            query = query.filter_by(user_id=petition_filter.user_id)

        return await self._session.scalar(query)
