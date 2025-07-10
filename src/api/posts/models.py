from models import Base, DateMixin


class Post(Base, DateMixin):
    __tablename__ = "posts"

