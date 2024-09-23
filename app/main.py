from fastapi import FastAPI
from app.core.deps import get_db
from app.core.settings import settings
from app.jwt_auth.router import JWTAuthentication


app = FastAPI()

jwt_auth = JWTAuthentication(
    jwt_secret=settings.JWT_SECRET,
    jwt_access_token_exp=settings.JWT_ACCESS_TOKEN_EXP_MINUTES,
    jwt_refresh_token_exp=settings.JWT_REFRESH_TOKEN_EXP_MINUTES,
    session_func=get_db,
)
app.include_router(jwt_auth.router, prefix="/auth", tags=["auth"])
