from typing import Sequence
from uuid import UUID

from pydantic import BaseModel, EmailStr, constr

from app.constants.gender import Gender


class UserData(BaseModel):
    id: UUID
    first_name: constr(min_length=1, max_length=48, strip_whitespace=True)  # type: ignore
    last_name: constr(min_length=1, max_length=48, strip_whitespace=True)  # type: ignore
    email: EmailStr
    gender: Gender

    class Config:
        orm_mode = True


class UserRegister(BaseModel):
    first_name: constr(min_length=1, max_length=48, strip_whitespace=True)  # type: ignore
    last_name: constr(min_length=1, max_length=48, strip_whitespace=True)  # type: ignore
    email: EmailStr
    gender: Gender
    password: constr(min_length=8, max_length=24)  # type: ignore


class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=24)  # type: ignore


class UsersPage(BaseModel):
    current_page: int
    pages_count: int
    page_limit: int
    users: Sequence[UserData]

    class Config:
        orm_mode = True
