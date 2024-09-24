from collections.abc import AsyncGenerator, Callable
from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from .auth_service import AuthenticationService
from .schemas import LoginIn, RefreshTokenIn, TokenPair, UserCreationSchema, UserSchema

security = HTTPBearer(auto_error=False)


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
        jwt_access_token_exp: int = 20,
        jwt_refresh_token_exp: int = 24 * 60,
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
            return AuthenticationService(
                session, jwt_secret, jwt_access_token_exp, jwt_refresh_token_exp
            )

        self._get_auth_service = get_auth_service

        self._create_routes(login_url, register_url, me_url, refresh_token_url)

    @property
    def get_current_user(self):
        async def inner(
            authorization: Annotated[
                Union[HTTPAuthorizationCredentials, None], Depends(security)
            ],
            auth_service: Annotated[
                AuthenticationService, Depends(self._get_auth_service)
            ],
        ) -> UserSchema:
            if authorization is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            user = await auth_service.get_user_from_token(authorization.credentials)
            if user is None:
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
            return user

        return inner

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
            access_token = auth_service.generate_access_token_for_user(user)
            refresh_token = auth_service.generate_refresh_token_for_user(user)
            return TokenPair(access_token=access_token, refresh_token=refresh_token)

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
        async def get_info_about_current_user(
            current_user: Annotated[UserSchema, Depends(self.get_current_user)],
        ) -> UserSchema:
            return current_user

        @self._router.post(refresh_token_url)
        async def refresh_token(data: RefreshTokenIn) -> TokenPair:
            return TokenPair(access_token="fake", refresh_token="fake")

    @property
    def router(self) -> APIRouter:
        return self._router
