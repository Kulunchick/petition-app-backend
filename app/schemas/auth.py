from pydantic import BaseModel, EmailStr, constr

from app.schemas.user import UserData
from app.types.gender import Gender


class UserLogged(UserData, BaseModel):
    token: bytes

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=24)  # type: ignore


class UserRegister(BaseModel):
    first_name: constr(min_length=1, max_length=48, strip_whitespace=True)  # type: ignore
    last_name: constr(min_length=1, max_length=48, strip_whitespace=True)  # type: ignore
    email: EmailStr
    gender: Gender
    password: constr(min_length=8, max_length=24)  # type: ignore
