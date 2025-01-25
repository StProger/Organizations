from pydantic_settings import BaseSettings
from pydantic import Field


class Config(BaseSettings):

    postgres_port: int = Field(alias='POSTGRES_PORT')
    postgres_db: str = Field(alias='POSTGRES_DB')
    postgres_user: str = Field(alias='POSTGRES_USER')
    postgres_password: str = Field(alias='POSTGRES_PASSWORD')
    postgres_host: str = Field(alias='POSTGRES_HOST')

    @property
    def database_dsn(self) -> str:
        return (
            f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}'
            f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'
        )


config = Config()