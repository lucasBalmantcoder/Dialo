"""add timestamp column to audit_log

Revision ID: 8b85c8b605ba
Revises: 026f9a51dcc8
Create Date: 2025-06-24 11:16:34.836273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b85c8b605ba'
down_revision = '026f9a51dcc8'
branch_labels = None
depends_on = None


def upgrade():
     op.add_column('audit_log', sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')))


def downgrade():
    op.drop_column('audit_log', 'timestamp')
