from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    POSTGRES_HOST: str

    @property
    def postgres_dsn(self: 'Settings') -> str:
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}'
            f':{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}'
            f':{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )

settings = Settings()
