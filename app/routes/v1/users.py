import math
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.types.positive_int import PositiveInt
from app.security.security import get_user
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


@router.get("/")
async def get_users(page: PositiveInt = 1, page_limit: PositiveInt = 50, session: AsyncSession = Depends(get_session)) -> UsersPage:
    user_repository = UserRepository(session)
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
async def get_me(user: User = Depends(get_user)) -> UserData:
    return UserData.from_orm(user)


@router.get("/{user_id}")
async def get_user(user_id: UUID, session: AsyncSession = Depends(get_session)) -> UserData:
    user_repository = UserRepository(session)
    user = await user_repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Not found")

    return UserData.from_orm(user)


@router.get("/{user_id}/petitions")
async def get_user_petitions(user_id: UUID, page: PositiveInt, page_limit: PositiveInt, session: AsyncSession = Depends(get_session)) -> PetitionsPage:
    petition_repository = PetitionRepository(session)

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
