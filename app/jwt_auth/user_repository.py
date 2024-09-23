from typing import Union
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .user_model import User


class UserRepository:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(User.id == user_id)
        results = await self._session.execute(query)
        return results.scalar_one_or_none()

    async def get_user_by_email(self, user_email: str) -> Union[User, None]:
        query = select(User).where(User.email == user_email)
        results = await self._session.execute(query)
        return results.scalar_one_or_none()

    async def create_user_and_commit(self, user_email: str, hashed_password: str) -> Union[User, None]:
        user = User(email=user_email, hashed_password=hashed_password)
        self._session.add(user)

        try:
            await self._session.commit()
            await self._session.refresh(user)
            return user
        except IntegrityError:
            await self._session.rollback()
            return None
