import math
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_restful.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.types.positive_int import PositiveInt
from app.security.utils import get_user
from app.database import get_session
from app.models import User, Petition
from app.repositories.petition import PetitionRepository, PetitionFilter
from app.repositories.user import UserRepository
from app.schemas.petition import PetitionsPage, PetitionData
from app.schemas.user import UserData, UsersPage

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@cbv(router)
class UsersController:
    session: AsyncSession = Depends(get_session)

    @router.get("/")
    async def get_users(self, page: PositiveInt = 1, page_limit: PositiveInt = 50) -> UsersPage:
        user_repository = UserRepository(self.session)
        count = await user_repository.get_count()
        if count is None:
            raise HTTPException(status_code=500, detail="Error")

        pages_count = math.ceil(count / page_limit)
        if pages_count < page:
            raise HTTPException(status_code=404, detail="Not found")

        users = await user_repository.get(
            limit=page_limit,
            offset=page_limit * (page - 1)
        )

        return UsersPage(
            current_page=page,
            page_limit=page_limit,
            pages_count=pages_count or 1,
            users=[UserData.from_orm(user) for user in users]
        )

    @router.get("/me")
    async def get_me(self, user: User = Depends(get_user)) -> UserData:
        return UserData.from_orm(user)

    @router.get("/{user_id}")
    async def get_user(self, user_id: UUID) -> UserData:
        user_repository = UserRepository(self.session)
        user = await user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Not found")

        return UserData.from_orm(user)

    @router.get("/{user_id}/petitions")
    async def get_user_petitions(self, user_id: UUID, page: PositiveInt, page_limit: PositiveInt) -> PetitionsPage:
        petition_repository = PetitionRepository(self.session)

        count = await petition_repository.get_count_by_filter(PetitionFilter(user_id=user_id))
        if count is None:
            raise HTTPException(status_code=500, detail="Error")

        pages_count = math.ceil(count / page_limit)
        if pages_count < page:
            raise HTTPException(status_code=404, detail="Not found")

        petitions = await petition_repository.get(
            limit=page_limit,
            offset=page_limit * (page - 1),
            options=[selectinload(Petition.user)]
        )

        return PetitionsPage(
            current_page=page,
            page_limit=page_limit,
            pages_count=pages_count or 1,
            petitions=[PetitionData.from_orm(petition) for petition in petitions]
        )
