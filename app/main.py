from fastapi import FastAPI
from app.core.deps import get_db
from app.jwt_auth.router import JWTAuthentication


app = FastAPI()

jwt_auth = JWTAuthentication(jwt_secret='very_strong_key', session_func=get_db)
app.include_router(jwt_auth.router, prefix='/auth', tags=['auth'])
