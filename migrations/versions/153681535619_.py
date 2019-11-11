"""Add tags table and tags to the beer table

Revision ID: 153681535619
Revises: 1dc2f4c6ba3a
Create Date: 2015-06-07 17:23:03.861607

"""

# revision identifiers, used by Alembic.
revision = "153681535619"
down_revision = "1dc2f4c6ba3a"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user", sa.Integer(), nullable=True),
        sa.Column("beer", sa.Integer(), nullable=True),
        sa.Column("tag", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["user"], ["users.id"]),
        sa.ForeignKeyConstraint(["beer"], ["beers.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("tags")
