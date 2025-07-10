from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import UniqueConstraint, ForeignKey
from sqlalchemy.types import String

from models import Base, DateMixin


class Post(Base, DateMixin):
    __tablename__ = "posts"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[Optional[str]] = mapped_column(String(2048))

    __table_args__ = (
        UniqueConstraint(
            "title",
            "user_id",
            name="unique_title_with_user",
        ),
    )
