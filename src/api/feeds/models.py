from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base

if TYPE_CHECKING:
    from api.auth.users.models import User


class FeedType(StrEnum):
    follow = "FOLLOW"
    post = "POST"


class UserFeed(Base):
    __tablename__ = "users_feed"
    repr_cols_num = 10

    # Колонки
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    event_id: Mapped[int]
    event_type: Mapped[FeedType]

    # Отношения
    author: Mapped["User"] = relationship(
        "User",
        back_populates="feeds",
        primaryjoin="UserFeed.author_id == User.id"
    )
