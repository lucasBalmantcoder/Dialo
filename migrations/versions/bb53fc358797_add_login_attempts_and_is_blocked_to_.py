"""add login_attempts and is_blocked to user

Revision ID: bb53fc358797
Revises: faf4d8e9b1af
Create Date: 2025-06-24 23:00:29.025351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb53fc358797'
down_revision = 'faf4d8e9b1af'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('login_attempts', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('user', sa.Column('is_blocked', sa.Boolean(), nullable=False, server_default='false'))


def downgrade():
    pass
