from datetime import datetime
from datetime import timedelta
from typing import Union
from uuid import UUID

from authlib.jose import jwt
from authlib.jose.errors import DecodeError
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel, validator

from app.config import settings

ACCESS_TOKEN_EXPIRE_MINUTES = 7 * 60 * 60  # 7 days
ALGORITHM = "HS256"


class TokenData(BaseModel):
    sub: Union[UUID, str]
    exp: datetime

    @validator("sub")
    def validate_uuids(cls, value: Union[UUID, str]) -> Union[UUID, str]:
        if value:
            return str(value)
        return value


class JWTRepo:
    header = {
        "alg": ALGORITHM
    }

    @classmethod
    def create_access_token(cls, user_id: UUID) -> bytes:
        payload = TokenData(
            sub=user_id,
            exp=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return jwt.encode(cls.header, payload.dict(), settings.SECRET_KEY.get_secret_value())

    @classmethod
    def decode_jwt_token(cls, token: str):
        return jwt.decode(token, settings.SECRET_KEY.get_secret_value())


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=401, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = JWTRepo.decode_jwt_token(jwt_token)
        except DecodeError:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid
