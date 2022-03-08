"""add price fields to car object

Revision ID: a8af936a8a4d
Revises: cbc2b08a748b
Create Date: 2022-03-07 22:47:05.572963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8af936a8a4d'
down_revision = 'cbc2b08a748b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cars_info', sa.Column('price_usd', sa.Integer(), nullable=True))
    op.add_column('cars_info', sa.Column('price_uah', sa.Integer(), nullable=True))
    op.add_column('cars_info', sa.Column('price_eur', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cars_info', 'price_eur')
    op.drop_column('cars_info', 'price_uah')
    op.drop_column('cars_info', 'price_usd')
    # ### end Alembic commands ###
