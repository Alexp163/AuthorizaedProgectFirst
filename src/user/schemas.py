from datetime import datetime

from pydantic import BaseModel


class UserReadSchema(BaseModel):
    id: int
    nickname: str
    created_at: datetime
    updated_at: datetime

class UserCreateSchema(BaseModel):
    nickname: str
    password: str

class UserUpdateSchema(BaseModel):
    nickname: str
    password: str

class AccessTokenSchema(BaseModel):
    access_token: str
    token_type: str
