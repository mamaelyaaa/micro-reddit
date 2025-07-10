from typing import Optional, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from models import Base, DateMixin

if TYPE_CHECKING:
    from api.posts.models import Post


class User(Base, DateMixin):
    __tablename__ = "users"

    # Колонки
    username: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(128), unique=True)
    password: Mapped[Optional[str]]

    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    # Отношения
    user_posts: Mapped[list["Post"]] = relationship(back_populates="post_user")
