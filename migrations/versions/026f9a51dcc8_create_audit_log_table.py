"""create audit_log table

Revision ID: 026f9a51dcc8
Revises: c70a711d64f4
Create Date: 2025-06-24 00:02:00.439353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '026f9a51dcc8'
down_revision = 'c70a711d64f4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'audit_log',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), nullable=False),
        sa.Column('action', sa.String(length=255), nullable=False),
        sa.Column('details', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now())
    )


def downgrade():
    op.drop_table('audit_log')