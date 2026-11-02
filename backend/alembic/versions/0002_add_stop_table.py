"""add stop table

Revision ID: 0002
Revises: 0001
"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "stop",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("image_url", sa.String(255), nullable=True),
        sa.Column("is_transfer", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("x", sa.Float(), nullable=True),
        sa.Column("y", sa.Float(), nullable=True),
        sa.Column("wheelchair_accessible", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("has_shelter", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("has_bench", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("has_ticket_machine", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("has_display", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_table("stop")
