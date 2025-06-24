"""add timestamp column to audit_log 2

Revision ID: 7d1e80a10bce
Revises: 8b85c8b605ba
Create Date: 2025-06-24 11:21:17.896053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d1e80a10bce'
down_revision = '8b85c8b605ba'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('audit_log', sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')))


def downgrade():
    op.drop_column('audit_log', 'timestamp')
