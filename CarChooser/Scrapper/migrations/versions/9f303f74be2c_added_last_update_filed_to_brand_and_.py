"""Added last update filed to brand and model tables


Revision ID: 9f303f74be2c
Revises: bf37ecde804d
Create Date: 2022-03-23 22:55:03.408187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f303f74be2c'
down_revision = 'bf37ecde804d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('brands', sa.Column('last_update', sa.DateTime(), nullable=True))
    op.add_column('models', sa.Column('last_update', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('models', 'last_update')
    op.drop_column('brands', 'last_update')
    # ### end Alembic commands ###
