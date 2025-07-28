from pydantic import BaseModel, ConfigDict

from api.auth.users.schemas import UserSummaryReadSchema
from .models import FeedType
from ..posts.schemas import PostReadSchema


class FeedBaseSchema(BaseModel):
    author_id: int
    post_id: int


class FeedCreateSchema(FeedBaseSchema):
    pass


class FeedReadSchema(FeedBaseSchema):
    model_config = ConfigDict(from_attributes=True)


class FeedDetailSchema(BaseModel):
    # author_id: int
    # post_id: int
    author: UserSummaryReadSchema
    post: PostReadSchema

    model_config = ConfigDict(from_attributes=True)
