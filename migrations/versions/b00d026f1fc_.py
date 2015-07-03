"""Add default settings to User table

Revision ID: b00d026f1fc
Revises: 153681535619
Create Date: 2015-07-03 14:59:51.787121

"""

# revision identifiers, used by Alembic.
revision = 'b00d026f1fc'
down_revision = '153681535619'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('users', sa.Column('default_drink_date', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('default_drink_location_city', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('default_drink_location_country', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('users', 'default_drink_location_country')
    op.drop_column('users', 'default_drink_location_city')
    op.drop_column('users', 'default_drink_date')
