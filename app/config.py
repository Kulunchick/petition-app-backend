from typing import Optional

from pydantic import BaseSettings, SecretStr, PositiveInt


class Settings(BaseSettings):
    LOGLEVEL: Optional[str] = "DEBUG"
    POSTGRES_HOST: str
    POSTGRES_PORT: PositiveInt
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str

    class Config:
        env_file = ".env", "stack.env"
        env_file_encoding = "utf-8"
