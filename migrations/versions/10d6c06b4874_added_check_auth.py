"""Added check auth

Revision ID: 10d6c06b4874
Revises: f93440d5c5be
Create Date: 2025-03-24 10:37:28.947211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10d6c06b4874'
down_revision = 'f93440d5c5be'
branch_labels = None
depends_on = None


def upgrade():
    # Allow NULL values temporarily
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('difficulty', sa.String(length=20), nullable=True))  

    with op.batch_alter_table('leaderboard', schema=None) as batch_op:
        batch_op.add_column(sa.Column('difficulty', sa.String(length=20), nullable=True))  

    # Set a default value for existing records
    op.execute("UPDATE game SET difficulty = 'easy' WHERE difficulty IS NULL")
    op.execute("UPDATE leaderboard SET difficulty = 'easy' WHERE difficulty IS NULL")

    # Now enforce NOT NULL constraint
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.alter_column('difficulty', nullable=False)

    with op.batch_alter_table('leaderboard', schema=None) as batch_op:
        batch_op.alter_column('difficulty', nullable=False)


def downgrade():
    with op.batch_alter_table('leaderboard', schema=None) as batch_op:
        batch_op.drop_column('difficulty')

    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.drop_column('difficulty')
