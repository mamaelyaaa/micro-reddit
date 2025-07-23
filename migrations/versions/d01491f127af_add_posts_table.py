"""add posts table

Revision ID: d01491f127af
Revises: 276d73e41be4
Create Date: 2025-07-10 23:01:38.112718

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d01491f127af"
down_revision: Union[str, Sequence[str], None] = "276d73e41be4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("description", sa.String(length=2048), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title", "user_id", name="unique_title_with_user"),
    )
    op.create_index(op.f("ix_posts_id"), "posts", ["id"], unique=False)
    op.drop_constraint(op.f("users_username_key"), "users", type_="unique")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_unique_constraint(
        op.f("users_username_key"),
        "users",
        ["username"],
        postgresql_nulls_not_distinct=False,
    )
    op.drop_index(op.f("ix_posts_id"), table_name="posts")
    op.drop_table("posts")
