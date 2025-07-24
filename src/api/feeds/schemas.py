from pydantic import BaseModel, ConfigDict

from .models import FeedType


class FeedBaseSchema(BaseModel):
    author_id: int
    event_id: int
    event_type: FeedType


class FeedCreateSchema(FeedBaseSchema):
    pass


class FeedReadSchema(FeedBaseSchema):
    model_config = ConfigDict(from_attributes=True)
