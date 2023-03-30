from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')


class IBaseRepository(ABC):
    @property
    def __model__(self):
        raise NotImplementedError

    @abstractmethod
    async def create(self):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, model_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def update(self, model_id: UUID, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, model_id: UUID):
        raise NotImplementedError


class BaseRepository(IBaseRepository, Generic[T]):
    __model__: T

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create(self, **kwargs):
        model = self.__model__(**kwargs)
        self.__session.add(model)
        return model

    async def get_all(self):
        query = select(self.__model__)
        return (await self.__session.scalars(query)).all()

    async def get_by_id(self, model_id: UUID):
        return self.__session.get(self.__model__, model_id)

    async def update(self, model_id: UUID, **kwargs):
        query = update(self.__model__)\
            .where(self.__model__.id == model_id)\
            .values(**kwargs)\
            .execution_options(synchronize_session="evaluate")
        return await self.__session.execute(query)

    async def delete(self, model_id: UUID):
        query = delete(self.__model__).where(self.__model__.id == model_id)
        return await self.__session.execute(query)
