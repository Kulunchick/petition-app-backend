import math
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_restful.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_session
from app.models import User, Petition
from app.repositories.petition import PetitionRepository
from app.repositories.vote import VoteRepository, VoteFilter
from app.schemas.petition import PetitionsPage, NewPetition, PetitionData, UpdatePetition
from app.security.utils import get_user
from app.types.positive_int import PositiveInt

router = APIRouter(
    prefix="/petitions",
    tags=["petitions"]
)


@cbv(router)
class PetitionsController:
    session: AsyncSession = Depends(get_session)

    @router.get("/")
    async def get_petitions(self, page: PositiveInt = 1, page_limit: PositiveInt = 50,) -> PetitionsPage:
        petition_repository = PetitionRepository(self.session)

        count = await petition_repository.get_count()
        if count is None:
            raise HTTPException(status_code=500, detail="Error")

        pages_count = math.ceil(count / page_limit) or 1
        if pages_count < page:
            raise HTTPException(status_code=404, detail="Not found")

        petitions = await petition_repository.get(
            limit=page_limit,
            offset=page_limit * (page - 1),
            options=[selectinload(Petition.user)],
            order=[Petition.created_at.desc()]
        )

        response = PetitionsPage(
            current_page=page,
            page_limit=page_limit,
            pages_count=pages_count,
            petitions=[]
        )
        vote_repository = VoteRepository(self.session)
        for petition in petitions:
            petition = PetitionData.from_orm(petition)
            petition.votes_count = await vote_repository.get_count_by_filter(VoteFilter(petition_id=petition.id))
            response.petitions.append(petition)

        return response

    @router.get("/{petition_id}")
    async def get_petition(self, petition_id: UUID):
        petition_repository = PetitionRepository(self.session)
        petition = await petition_repository.get_by_id(
            petition_id,
            [selectinload(Petition.user)]
        )
        if petition is None:
            return HTTPException(status_code=404, detail="Not found")

        response = PetitionData.from_orm(petition)

        vote_repository = VoteRepository(self.session)
        response.votes_count = await vote_repository.get_count_by_filter(VoteFilter(petition_id=petition_id))

        return response

    @router.post("/")
    async def add_petition(self, new_petition: NewPetition, user: User = Depends(get_user)) -> PetitionData:
        petition_repository = PetitionRepository(self.session)
        petition = Petition(
            title=new_petition.title,
            description=new_petition.description,
            user_id=user.id
        )
        await petition_repository.create(petition)
        await self.session.flush()

        return PetitionData.from_orm(petition)

    @router.put("/{petition_id}")
    async def update_petition(self, petition_id: UUID, update: UpdatePetition, user: User = Depends(get_user)) -> PetitionData:
        petition_repository = PetitionRepository(self.session)
        petition = await petition_repository.get_by_id(
            petition_id,
            [selectinload(Petition.user)]
        )
        if petition is None:
            raise HTTPException(status_code=404, detail="Not found")

        if petition.user_id != user.id:
            raise HTTPException(status_code=403, detail="You can't edit not your petitions")

        if update.title is not None:
            petition.title = update.title
        if update.description is not None:
            petition.description = update.description

        return PetitionData.from_orm(petition)

    @router.delete("/{petition_id}")
    async def delete_petition(self, petition_id: UUID, user: User = Depends(get_user)) -> PetitionData:
        petition_repository = PetitionRepository(self.session)
        petition = await petition_repository.get_by_id(
            petition_id,
            options=[selectinload(Petition.user)]
        )
        if petition is None:
            raise HTTPException(status_code=404, detail="Not found")

        if petition.user_id != user.id:
            raise HTTPException(status_code=403, detail="You can't delete not your petitions")

        await petition_repository.delete(petition_id)

        return PetitionData.from_orm(petition)
