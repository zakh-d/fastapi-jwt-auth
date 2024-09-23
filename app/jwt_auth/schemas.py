from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


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
    email: str
    created_at: datetime


class UserCreationSchema(BaseModel):
    @model_validator(mode="after")
    def check_passwords_match(self):
        pw1 = self.password
        pw2 = self.password_confirmation

        if pw1 is None or pw2 is None or pw1 != pw2:
            raise ValueError("passwords don't match")
        return self

    email: EmailStr
    password: str = Field(max_length=250, min_length=8)
    password_confirmation: str = Field(max_length=250)
