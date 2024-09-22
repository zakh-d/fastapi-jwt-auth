from collections.abc import AsyncGenerator, Callable

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import RefreshTokenIn, TokenPair


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
        me_url: str = "/me",
        refresh_token_url: str = "/refresh",
    ):
        self._router = APIRouter()
        self._secret = jwt_secret
        self._create_routes(login_url, me_url, refresh_token_url)
        self._session = session_func

    def _create_routes(
        self, login_url: str, me_url: str, refresh_token_url: str
    ) -> None:
        @self._router.post(login_url)
        async def login_user() -> TokenPair:
            return TokenPair(access_token="fake", refresh_token="fake")

        @self._router.get(me_url)
        async def get_info_about_current_user():
            return {"message": "Not Implemented"}

        @self._router.post(refresh_token_url)
        async def refresh_token(data: RefreshTokenIn) -> TokenPair:
            return TokenPair(access_token="fake", refresh_token="fake")

    @property
    def router(self) -> APIRouter:
        return self._router
