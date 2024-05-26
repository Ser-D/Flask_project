"""Init

Revision ID: af11506e5d81
Revises: 
Create Date: 2024-05-26 14:33:46.076009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af11506e5d81'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=64), nullable=False),
    sa.Column('group', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('ticket',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=64), nullable=False),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('user_create', sa.Integer(), nullable=True),
    sa.Column('group_work', sa.String(length=64), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_create'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_ticket_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_ticket_timestamp'))

    op.drop_table('ticket')
    op.drop_table('user')
    # ### end Alembic commands ###
