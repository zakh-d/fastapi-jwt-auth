from fastapi import APIRouter

from app.jwt_auth.schemas import TokenPair


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
    def __init__(self, jwt_secret: str, login_url: str = "/login", me_url: str = "/me"):
        self._router = APIRouter()
        self._secret = jwt_secret
        self._create_routes(login_url, me_url)

    def _create_routes(self, login_url: str, me_url: str) -> None:
        @self._router.post(login_url)
        async def login_user() -> TokenPair:
            return TokenPair(access_token="fake", refresh_token="fake")

        @self._router.get(me_url)
        async def get_info_about_current_user():
            return {"message": "Not Implemented"}

    @property
    def router(self) -> APIRouter:
        return self._router
