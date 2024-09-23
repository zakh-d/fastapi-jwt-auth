from collections.abc import AsyncGenerator, Callable
from typing import Annotated

from app.jwt_auth.auth_service import AuthenticationService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import LoginIn, RefreshTokenIn, TokenPair, UserCreationSchema, UserSchema


class JWTAuthentication:
    """
    This class provides you with jwt authentication functionality:

    usage:
    ```python
    from fastapi import FastAPI
    from jwt_auth.router import JWTAuthentication

    auth = JWTAuthentication(jwt_secret='your_secret_key')

    app = FastAPI()
    app.include_router(auth.router, prefix='auth', tags=['auth'])
    ```
    """

    def __init__(
        self,
        jwt_secret: str,
        session_func: Callable[[], AsyncGenerator[AsyncSession, None]],
        login_url: str = "/login",
        register_url: str = "/register",
        me_url: str = "/me",
        refresh_token_url: str = "/refresh",
    ):
        self._router = APIRouter()
        self._secret = jwt_secret
        self._session_func = session_func

        def get_auth_service(
            session: Annotated[AsyncSession, Depends(self._session_func)],
        ) -> AuthenticationService:
            return AuthenticationService(session)

        self._get_auth_service = get_auth_service

        self._create_routes(login_url, register_url, me_url, refresh_token_url)

    def _create_routes(
        self, login_url: str, register_url: str, me_url: str, refresh_token_url: str
    ) -> None:
        @self._router.post(login_url)
        async def login_user(
            login_data: LoginIn,
            auth_service: Annotated[
                AuthenticationService, Depends(self._get_auth_service)
            ],
        ) -> TokenPair:
            user = await auth_service.login_user(login_data.email, login_data.password)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid credentials were provided",
                )
            return TokenPair(access_token="fake", refresh_token="fake")

        @self._router.post(register_url, status_code=status.HTTP_201_CREATED)
        async def register_user(
            registration_data: UserCreationSchema,
            auth_service: Annotated[
                AuthenticationService, Depends(self._get_auth_service)
            ],
        ) -> UserSchema:
            user = await auth_service.register_user(
                registration_data.email, registration_data.password
            )
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={"conflict_field": "email"},
                )
            return user

        @self._router.get(me_url)
        async def get_info_about_current_user():
            return {"message": "Not Implemented"}

        @self._router.post(refresh_token_url)
        async def refresh_token(data: RefreshTokenIn) -> TokenPair:
            return TokenPair(access_token="fake", refresh_token="fake")

    @property
    def router(self) -> APIRouter:
        return self._router
