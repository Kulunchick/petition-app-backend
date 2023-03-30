from pydantic import EmailStr
from sqlalchemy import select, update

from app.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    __model__ = User

    async def find_by_username(self, username: str):
        query = select(self.__model__).filter_by(username=username).limit(1)
        return (await self.__session.scalars(query)).first()

    async def find_by_email(self, email: EmailStr):
        query = select(self.__model__).filter_by(email=email)
        return (await self.__session.scalars(query)).first()

    async def update_password(self, email: EmailStr, password: str):
        query = update(self.__model__).filter_by(email=email).values(password=password)
        return await self.__session.execute(query)
