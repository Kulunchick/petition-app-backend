from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from fastapi_restful.cbv import cbv

from app.security.hashing import Hasher
from app.security.security import JWTRepo
from app.database import get_session
from app.models import User
from app.repositories.user import UserRepository, UserFilter
from app.schemas.auth import UserLogged, UserLogin, UserRegister

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@cbv(router)
class AuthController:
    session: AsyncSession = Depends(get_session)

    @router.post("/login")
    async def login(self, credentials: UserLogin) -> UserLogged:
        user_repository = UserRepository(self.session)
        user = await user_repository.find_one(UserFilter(email=credentials.email))
        if user is None:
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        if not Hasher.verify_password(credentials.password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect email or password")

        token = JWTRepo.create_access_token(user.id)

        return UserLogged(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            gender=user.gender,
            token=token
        )

    @router.post("/register")
    async def register(self, credentials: UserRegister):
        user_repository = UserRepository(self.session)
        user = await user_repository.find_one(UserFilter(email=credentials.email))
        if user is not None:
            raise HTTPException(status_code=409, detail="User already exists")

        user = User(
            first_name=credentials.first_name,
            last_name=credentials.last_name,
            email=credentials.email,
            gender=credentials.gender,
            password=Hasher.get_password_hash(credentials.password)
        )
        await user_repository.create(user)

        return JSONResponse(status_code=201, content={"message": "Registered"})
