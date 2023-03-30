from app.models import Vote
from app.repositories.base import BaseRepository


class VoteRepository(BaseRepository):
    __model__ = Vote
