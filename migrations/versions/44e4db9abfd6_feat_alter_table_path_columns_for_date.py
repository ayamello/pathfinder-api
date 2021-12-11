"""feat: alter table path columns for date

Revision ID: 44e4db9abfd6
Revises: edc2c5653621
Create Date: 2021-12-10 22:48:36.963959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44e4db9abfd6'
down_revision = 'edc2c5653621'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_paths_end_date'), 'paths', ['end_date'], unique=False)
    op.create_index(op.f('ix_paths_initial_date'), 'paths', ['initial_date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_paths_initial_date'), table_name='paths')
    op.drop_index(op.f('ix_paths_end_date'), table_name='paths')
    # ### end Alembic commands ###
