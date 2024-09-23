from typing import Union

from passlib.hash import argon2
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserSchema
from .user_repository import UserRepository


class AuthenticationService:
    def __init__(self, session: AsyncSession):
        self._user_repo = UserRepository(session)

        # argon configuration according to OWASP recommendations on password storage as for Sep 2024
        self._argon2_hasher = argon2.using(
            type="ID", rounds=2, memory_cost=19 * 1024, parallelism=1
        )

    async def login_user(self, email: str, password: str) -> Union[UserSchema, None]:
        user = await self._user_repo.get_user_by_email(email)
        if user is None:
            # simulate password hashing to prevent enumeration attack
            _ = self._argon2_hasher.hash(password)
            return None
        if not self._argon2_hasher.verify(password, user.hashed_password):
            return None
        return UserSchema.model_validate(user)

    async def register_user(self, email: str, password: str) -> Union[UserSchema, None]:
        hashed_password = self._argon2_hasher.hash(password)
        user = await self._user_repo.create_user_and_commit(email, hashed_password)

        if user is None:
            return None

        return UserSchema.model_validate(user)
