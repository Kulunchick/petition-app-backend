from datetime import datetime
from typing import Sequence

from pydantic import BaseModel

from app.schemas.petition import PetitionData
from app.schemas.user import UserData


class PetitionVote(BaseModel):
    user: UserData
    created_at: datetime

    class Config:
        orm_mode = True


class VoteData(PetitionVote):
    petition: PetitionData


class VotesPage(BaseModel):
    current_page: int
    pages_count: int
    page_limit: int
    votes: Sequence[PetitionVote]


class CheckVote(BaseModel):
    can_vote: bool
    is_your_petition: bool
