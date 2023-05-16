from pydantic import BaseModel

from app.schemas.user import UserData


class UserLogged(UserData, BaseModel):
    token: bytes

    class Config:
        orm_mode = True
