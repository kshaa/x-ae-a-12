"""Messaging model

Revision ID: a72f4baf9084
Revises: 0001c8ac1a69
Create Date: 2020-05-15 14:12:48.340860

"""

# revision identifiers, used by Alembic.
revision = 'a72f4baf9084'
down_revision = '0001c8ac1a69'

from alembic import op
import sqlalchemy as sa

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apikeys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_user_id', sa.Integer(), nullable=True),
    sa.Column('key', sa.String(length=512), server_default='', nullable=False),
    sa.Column('label', sa.String(length=512), server_default='', nullable=False),
    sa.ForeignKeyConstraint(['owner_user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key')
    )
    op.create_table('topics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_user_id', sa.Integer(), nullable=True),
    sa.Column('code', sa.String(length=50), server_default='', nullable=False),
    sa.Column('label', sa.Unicode(length=255), server_default='', nullable=True),
    sa.ForeignKeyConstraint(['owner_user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('topic_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.Unicode(length=255), server_default='', nullable=True),
    sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_table('topics')
    op.drop_table('apikeys')
    # ### end Alembic commands ###
