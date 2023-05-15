from typing import Sequence, Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.sql.base import ExecutableOption

from app.models import Vote
from app.repositories.base import BaseRepository


class VoteFilter(BaseModel):
    user_id: Optional[UUID]
    petition_id: Optional[UUID]


class VoteRepository(BaseRepository[Vote]):
    __model__ = Vote

    async def find(
            self,
            vote_filter: VoteFilter,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Sequence[Vote]:
        query = select(self.__model__)

        if vote_filter.user_id is not None:
            query = query.filter_by(user_id=vote_filter.user_id)
        if vote_filter.petition_id is not None:
            query = query.filter_by(petition_id=vote_filter.petition_id)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).all()

    async def find_one(
            self,
            vote_filter: VoteFilter,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Optional[Vote]:
        query = select(self.__model__).limit(1)

        if vote_filter.user_id is not None:
            query = query.filter_by(user_id=vote_filter.user_id)
        if vote_filter.petition_id is not None:
            query = query.filter_by(petition_id=vote_filter.petition_id)
        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).first()

    async def get_count_by_filter(self, vote_filter: VoteFilter) -> Optional[int]:
        query = select(func.count()).select_from(self.__model__)

        if vote_filter.user_id is not None:
            query = query.filter_by(user_id=vote_filter.user_id)
        if vote_filter.petition_id is not None:
            query = query.filter_by(petition_id=vote_filter.petition_id)

        return await self._session.scalar(query)
