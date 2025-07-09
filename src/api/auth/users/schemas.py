from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_superuser: bool = False


class UserCreateSchema(UserBaseSchema):
    pass


class UserReadSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_superuser: bool = False
    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    username: str
    email: EmailStr
    is_superuser: bool
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class UserUpdatePartialSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_superuser: Optional[bool] = None
    is_active: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)
