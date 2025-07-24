from pydantic import BaseModel, ConfigDict


class FollowBaseSchema(BaseModel):
    follower_id: int
    followee_id: int


class FollowCreateSchema(FollowBaseSchema):
    pass


class FollowReadSchema(FollowBaseSchema):
    model_config = ConfigDict(from_attributes=True)
