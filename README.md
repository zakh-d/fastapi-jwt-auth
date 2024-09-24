# FastAPI JWT Authentication application
My goal was to create a JTW Authentication module for FastAPI that is easy to add to either new project or existing one.

Technology stack:
- FastAPI
- SQLAlchemy (with async api)
- Alembic

## How to use it
- Add app/jwt_auth directory into your project
- Connect JWT authentication to your FastAPI app by including router
 ```python
    from fastapi import FastAPI
    
    from app.deps import get_db_session  # async generator that yields AsyncSession
    from app.jwt_auth.router import JWTAuthentication

    auth = JWTAuthentication(jwt_secret='your_secret_key', session_func=get_db_session)

    app = FastAPI()
    app.include_router(auth.router, prefix='auth', tags=['auth'])
 ```
- Change SQLAlchemy Base import in [app/jwt_auth/user_model.py](app/jwt_auth/user_model.py) model
```python
# replace this
from app.core.db import ModelBase

# with your location of SQLAlchemy Base class, i.e.
from app.db import Base 
```
- Make sure to import User model in env.py file in Alembic configuration
```python
# alembic/env.py or something like that
...
from app.jwt_auth.user_model import User  # noqa: F401
...
```

## How to run this repo
You can use docker to run example app 
```
docker compose up -d --build
```
you might need to add sudo in case of linux system
