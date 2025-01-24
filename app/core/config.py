from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: Literal["prod", "dev", "qa", "stg", "local"] = "local"

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_PORT: int | str = 5432
    DATABASE_HOST: str = "localhost"

    DATABASE_URL: str

    # JWT Secret Key and Algorithm
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 999999
    
    OPENAI_API_KEY:str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
