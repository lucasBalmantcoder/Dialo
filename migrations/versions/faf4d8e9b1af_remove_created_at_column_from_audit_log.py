"""remove created_at column from audit_log

Revision ID: faf4d8e9b1af
Revises: 7d1e80a10bce
Create Date: 2025-06-24 11:36:53.255053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'faf4d8e9b1af'
down_revision = '7d1e80a10bce'
branch_labels = None
depends_on = None


def upgrade():
     op.drop_column('audit_log', 'created_at')


def downgrade():
    op.add_column('audit_log', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')))
