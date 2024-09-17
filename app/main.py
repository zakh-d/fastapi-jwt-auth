from fastapi import FastAPI
from jwt_auth.router import JWTAuthentication


app = FastAPI()

jwt_auth = JWTAuthentication(jwt_secret='very_strong_key')
app.include_router(jwt_auth.router, prefix='/auth', tags=['auth'])
