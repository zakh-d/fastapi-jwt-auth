from sqlalchemy import NullPool
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.core.settings import settings

engine = create_async_engine(settings.postgres_dsn, poolclass=NullPool)

# Create the async session
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class ModelBase(DeclarativeBase):
    pass
