from datetime import datetime
from typing import Optional, List
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
    title: constr(min_length=1, strip_whitespace=True)
    description: constr(min_length=1, strip_whitespace=True)
    created_at: datetime
    votes_count: Optional[int]
    user: UserData

    class Config:
        orm_mode = True


class PetitionsPage(BaseModel):
    current_page: int
    pages_count: int
    page_limit: int
    petitions: List[PetitionData]
