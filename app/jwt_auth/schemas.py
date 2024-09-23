from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenIn(BaseModel):
    refresh_token: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(max_length=250)


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: UUID
    created_at: datetime
