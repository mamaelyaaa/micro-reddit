from pydantic import BaseModel


class BaseResponseSchema(BaseModel):
    detail: str
