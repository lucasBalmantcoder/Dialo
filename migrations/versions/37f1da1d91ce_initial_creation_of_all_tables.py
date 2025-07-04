"""initial creation of all tables

Revision ID: 37f1da1d91ce
Revises: 
Create Date: 2025-07-04 21:59:39.598875

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37f1da1d91ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('audit_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('action', sa.String(length=255), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('details', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('is_confirmed', sa.Boolean(), nullable=True),
    sa.Column('password_with_hash', sa.String(length=100), nullable=False),
    sa.Column('login_attempts', sa.Integer(), nullable=True),
    sa.Column('is_blocked', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('public_key', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=100), nullable=False),
    sa.Column('created', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('created_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['created_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('room_user_association',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['room.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('room_user_association')
    op.drop_table('room')
    op.drop_table('message')
    op.drop_table('user')
    op.drop_table('audit_log')
    # ### end Alembic commands ###
