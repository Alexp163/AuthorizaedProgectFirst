from datetime import datetime

from pydantic import BaseModel


class ProductReadSchema(BaseModel):
    id: int
    title: str
    data: str
    user_id: int | None
    created_at: datetime
    updated_at: datetime


class ProductCreateSchema(BaseModel):
    title: str
    data: str
    user_id: int


class ProductUpdateSchema(BaseModel):
    title: str
    data: str




