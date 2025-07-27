from typing import Any

from pydantic import BaseModel, ConfigDict

from .models import FeedType
from ..auth.users.schemas import UserSummaryReadSchema


class FeedBaseSchema(BaseModel):
    author_id: int
    event_id: int
    event_type: FeedType


class FeedCreateSchema(FeedBaseSchema):
    pass


class FeedReadSchema(FeedBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class FeedDetailSchema(BaseModel):
    author_id: int
    event_id: int
    event_type: FeedType
    author: UserSummaryReadSchema

    model_config = ConfigDict(from_attributes=True)
