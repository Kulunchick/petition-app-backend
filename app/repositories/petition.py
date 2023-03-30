from abc import ABC, abstractmethod

from sqlalchemy import select

from app.models import Petition
from app.repositories.base import BaseRepository, IBaseRepository


class PetitionRepository(BaseRepository[Petition]):
    __model__ = Petition

    async def find_by_title(self, title: str, full_text: bool = False):
        query = select(self.__model__).limit(1)
        if full_text:
            query = query.where(self.__model__.title.like(f"%{title}%"))
        else:
            query = query.where(self.__model__.title == title)

        return (await self.__session.scalars(query)).first()

    async def get_all(self, limit: int = None, offset: int = None):
        query = select(self.__model__)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        return (await self.__session.scalars(query)).all()

    async def find_all_by_title(self, title: str, full_text: bool = False, limit: int = None, offset: int = 0):
        query = select(self.__model__)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        if full_text:
            query = query.where(self.__model__.title.like(f"%{title}%"))
        else:
            query = query.where(self.__model__.title == title)

        return (await self.__session.scalars(query)).all()
