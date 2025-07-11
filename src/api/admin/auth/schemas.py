from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class AdminUserUpdateSchema(BaseModel):
    username: str
    email: EmailStr
    is_superuser: bool
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class AdminUserUpdatePartialSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_superuser: Optional[bool] = None
    is_active: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)
