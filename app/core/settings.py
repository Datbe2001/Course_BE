from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    POSTGRES_HOST: str
    DEBUG: Optional[bool] = False

    ACCESS_TOKEN_EXPIRES_IN_DAYS: int
    REFRESH_TOKEN_EXPIRES_IN_DAYS: int
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str

    CLOUD_NAME: str
    API_KEY: str
    API_SECRET: str

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
