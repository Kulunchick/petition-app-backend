import math
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_restful.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_session
from app.models import User, Vote, Petition
from app.repositories.petition import PetitionRepository
from app.repositories.vote import VoteRepository, VoteFilter
from app.schemas.vote import VoteData, VotesPage, PetitionVote, CheckVote
from app.security.utils import get_user
from app.types.positive_int import PositiveInt

router = APIRouter(
    prefix="/votes",
    tags=["votes"]
)


@cbv(router)
class VotesController:
    session: AsyncSession = Depends(get_session)

    @router.get("/petitions/{petition_id}")
    async def get_votes(self, petition_id: UUID, page: PositiveInt = 1, page_limit: PositiveInt = 50) -> VotesPage:
        petition_repository = PetitionRepository(self.session)
        petition = await petition_repository.get_by_id(petition_id)
        if petition is None:
            raise HTTPException(status_code=404, detail="Not found")

        vote_repository = VoteRepository(self.session)
        count = await vote_repository.get_count()
        if count is None:
            raise HTTPException(status_code=500, detail="Error")

        pages_count = math.ceil(count / page_limit) or 1
        if pages_count < page:
            raise HTTPException(status_code=404, detail="Not found")

        votes = await vote_repository.find(
            VoteFilter(petition_id=petition_id),
            limit=page_limit,
            offset=page_limit * (page - 1),
            options=[selectinload(Vote.user), selectinload(Vote.petition).subqueryload(Petition.user)]
        )
        return VotesPage(
            current_page=page,
            page_limit=page_limit,
            pages_count=pages_count or 1,
            votes=[PetitionVote.from_orm(vote) for vote in votes]
        )

    @router.get("/petitions/{petition_id}/vote")
    async def vote_petition(self, petition_id: UUID, user: User = Depends(get_user)) -> VoteData:
        petition_repository = PetitionRepository(self.session)
        petition = await petition_repository.get_by_id(petition_id)
        if petition is None:
            raise HTTPException(status_code=404, detail="Not found")
        if petition.user_id == user.id:
            raise HTTPException(status_code=409, detail="You can't vote on your petition")

        vote_repository = VoteRepository(self.session)
        vote = await vote_repository.find_one(VoteFilter(petition_id=petition_id, user_id=user.id))
        if vote is not None:
            raise HTTPException(status_code=409, detail="You already voted")

        vote = Vote(
            user_id=user.id,
            petition_id=petition.id
        )
        await vote_repository.create(vote)
        await self.session.flush()
        await self.session.refresh(vote.petition, ["user"])

        return VoteData.from_orm(vote)

    @router.get("/petitions/{petition_id}/check")
    async def check(self, petition_id: UUID, user: User = Depends(get_user)) -> CheckVote:
        petition_repository = PetitionRepository(self.session)
        petition = await petition_repository.get_by_id(petition_id)
        if petition is None:
            raise HTTPException(status_code=404, detail="Not found")

        vote_repository = VoteRepository(self.session)
        vote = await vote_repository.find_one(VoteFilter(petition_id=petition_id, user_id=user.id))

        return CheckVote(
            can_vote=vote is None and petition.user_id != user.id,
            is_your_petition=petition.user_id == user.id
        )
