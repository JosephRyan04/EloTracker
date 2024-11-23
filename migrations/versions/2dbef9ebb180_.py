"""empty message

Revision ID: 2dbef9ebb180
Revises: 009a933942e5
Create Date: 2024-11-22 18:34:48.856945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2dbef9ebb180'
down_revision = '009a933942e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('LastCalculated', sa.DateTime(), nullable=False),
    sa.Column('MaxStreak', sa.Integer(), nullable=True),
    sa.Column('CurrentStreak', sa.Integer(), nullable=True),
    sa.Column('PeakGlobal', sa.Integer(), nullable=True),
    sa.Column('PeakRegional', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Stats', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Stats_LastCalculated'), ['LastCalculated'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Stats', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Stats_LastCalculated'))

    op.drop_table('Stats')
    # ### end Alembic commands ###