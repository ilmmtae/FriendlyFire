from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core.core_schema import ValidationInfo
from pydantic import field_validator
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env"))

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    POSTGRES_USER: str | None
    POSTGRES_PASSWORD: str | None
    POSTGRES_DB: str | None
    POSTGRES_HOST: str | None
    POSTGRES_PORT: str | None
    JWT_SECRET: str | None
    ALGORITHM: str | None
    REDIS_HOST: str | None
    REDIS_PORT: int | None
    BOT_TOKEN: str | None
    BOT_NAME: str | None
    HOST: str | None
    BROKER: str | None
    BACKEND: str | None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v, info: ValidationInfo) -> str:
        if isinstance(v, str):
            return v
        return (
            f"postgresql+asyncpg://{info.data['POSTGRES_USER']}:"
            f"{info.data['POSTGRES_PASSWORD']}@"
            f"{info.data['POSTGRES_HOST']}:"
            f"{info.data['POSTGRES_PORT']}/"
            f"{info.data['POSTGRES_DB']}"
        )

    SQLALCHEMY_DATABASE_URI: str | None = None

settings = Settings()