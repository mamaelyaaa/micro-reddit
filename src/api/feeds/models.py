from enum import StrEnum

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class FeedType(StrEnum):
    follow = "FOLLOW"
    post = "POST"


class UserFeed(Base):
    __tablename__ = "users_feed"

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    event_id: Mapped[int]
    event_type: Mapped[FeedType]
