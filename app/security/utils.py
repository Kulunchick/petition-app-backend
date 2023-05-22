from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import User
from app.repositories import UserRepository
from app.security.security import JWTBearer, TokenData, JWTRepo


async def get_user(token: str = Depends(JWTBearer()), session: AsyncSession = Depends(get_session)) -> User:
    user_repository = UserRepository(session)
    data = TokenData.parse_obj(JWTRepo.decode_jwt_token(token))

    user = await user_repository.get_by_id(UUID(data.sub))
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return user
