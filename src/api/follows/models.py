from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models import Base, DateMixin


class Follow(Base, DateMixin):
    __tablename__ = "follows"
    __table_args__ = (
        UniqueConstraint(
            "follower_id",
            "followee_id",
            name="unique_follows",
        ),
    )

    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    followee_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
