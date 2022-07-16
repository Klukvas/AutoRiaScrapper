"""added last upd to car and gearBox

Revision ID: ec397219321b
Revises: 9f303f74be2c
Create Date: 2022-03-27 17:52:28.008337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec397219321b'
down_revision = '9f303f74be2c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('gear_box', sa.Column('last_update', sa.DateTime(), nullable=True))
    op.add_column('cars_info', sa.Column('last_update', sa.DateTime(), nullable=True))



def downgrade():
    op.drop_column('gear_box', 'last_update')
    op.drop_column('cars_info', 'last_update')
