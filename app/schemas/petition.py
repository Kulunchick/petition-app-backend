from datetime import datetime
from typing import Optional, List, Any
from uuid import UUID

from pydantic import BaseModel, constr

from app.schemas.user import UserData


class NewPetition(BaseModel):
    title: str
    description: str


class UpdatePetition(BaseModel):
    title: Optional[str]
    description: Optional[str]


class PetitionData(BaseModel):
    id: UUID
    title: constr(min_length=1, strip_whitespace=True)  # type: ignore
    description: constr(min_length=1, strip_whitespace=True)  # type: ignore
    created_at: datetime
    votes_count: Optional[int]
    user: UserData

    class Config:
        orm_mode = True

    def dict(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        kwargs.pop('exclude_none', None)
        return super().dict(*args, exclude_none=True, **kwargs)


class PetitionsPage(BaseModel):
    current_page: int
    pages_count: int
    page_limit: int
    petitions: List[PetitionData]
