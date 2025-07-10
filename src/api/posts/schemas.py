from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PostBaseSchema(BaseModel):
    user_id: int
    title: str
    description: Optional[str]


class PostCreateSchema(PostBaseSchema):
    pass


class PostReadSchema(PostBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
