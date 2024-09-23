import datetime
from typing import Union

import jwt
from passlib.hash import argon2
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserSchema
from .user_repository import UserRepository


class AuthenticationService:
    def __init__(
        self,
        session: AsyncSession,
        jwt_secret: str,
        access_token_exp: int,
        refresh_token_exp: int,
    ):
        self._user_repo = UserRepository(session)

        # argon configuration according to OWASP recommendations on password storage as for Sep 2024
        self._argon2_hasher = argon2.using(
            type="ID", rounds=2, memory_cost=19 * 1024, parallelism=1
        )

        self._secret = jwt_secret
        self._access_token_exp = access_token_exp
        self._refresh_token_exp = refresh_token_exp

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

    def generate_access_token_for_user(self, user: UserSchema) -> str:
        expire_on = datetime.datetime.now() + datetime.timedelta(
            minutes=self._access_token_exp
        )
        payload = {
            "user_id": str(user.id),
            "exp": int(expire_on.timestamp()),
            "type": "access",
        }
        return jwt.encode(payload, self._secret, algorithm="HS256")

    def generate_refresh_token_for_user(self, user: UserSchema) -> str:
        expire_on = datetime.datetime.now() + datetime.timedelta(
            minutes=self._refresh_token_exp
        )
        payload = {
            "user_id": str(user.id),
            "exp": int(expire_on.timestamp()),
            "type": "refresh",
        }
        return jwt.encode(payload, self._secret, algorithm="HS256")
