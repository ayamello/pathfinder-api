"""merging three heads

Revision ID: 5a53b5b5a2bf
Revises: cedc62aaf675, c5f65ab0bd7b, ac76569e1c17
Create Date: 2021-12-14 23:00:43.949672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a53b5b5a2bf'
down_revision = ('cedc62aaf675', 'c5f65ab0bd7b', 'ac76569e1c17')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
