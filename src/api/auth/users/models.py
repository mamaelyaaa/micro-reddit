from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String

from models import Base, DateMixin


class User(Base, DateMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(128), unique=True)
    password: Mapped[Optional[str]]

    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
