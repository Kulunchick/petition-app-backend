from typing import Sequence
from uuid import UUID

from pydantic import BaseModel, EmailStr, constr

from app.types.gender import Gender


class UserData(BaseModel):
    id: UUID
    first_name: constr(min_length=1, max_length=48, strip_whitespace=True)  # type: ignore
    last_name: constr(min_length=1, max_length=48, strip_whitespace=True)  # type: ignore
    email: EmailStr
    gender: Gender

    class Config:
        orm_mode = True


class UsersPage(BaseModel):
    current_page: int
    pages_count: int
    page_limit: int
    users: Sequence[UserData]

    class Config:
        orm_mode = True
