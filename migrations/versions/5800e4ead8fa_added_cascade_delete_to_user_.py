"""Added cascade delete to User relationships

Revision ID: 5800e4ead8fa
Revises: 10d6c06b4874
Create Date: 2025-03-24 14:52:38.188165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5800e4ead8fa'
down_revision = '10d6c06b4874'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.drop_constraint('game_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('leaderboard', schema=None) as batch_op:
        batch_op.drop_constraint('leaderboard_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('leaderboard', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('leaderboard_user_id_fkey', 'user', ['user_id'], ['id'])

    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('game_user_id_fkey', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###
