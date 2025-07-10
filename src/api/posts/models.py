from typing import Optional, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import UniqueConstraint, ForeignKey
from sqlalchemy.types import String

from models import Base, DateMixin

if TYPE_CHECKING:
    from api.auth.users.models import User


class Post(Base, DateMixin):
    __tablename__ = "posts"

    # Колонки
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

    # Отношения
    post_user: Mapped["User"] = relationship(back_populates="user_posts")