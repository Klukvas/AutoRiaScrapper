"""added fields brand && model to car table

Revision ID: fc7a9a20997e
Revises: 51781f18df06
Create Date: 2022-03-07 19:16:50.951498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc7a9a20997e'
down_revision = '51781f18df06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cars_info', sa.Column('brand_id', sa.Integer(), nullable=True))
    op.add_column('cars_info', sa.Column('model_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'cars_info', 'models', ['model_id'], ['id'])
    op.create_foreign_key(None, 'cars_info', 'brands', ['brand_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cars_info', type_='foreignkey')
    op.drop_constraint(None, 'cars_info', type_='foreignkey')
    op.drop_column('cars_info', 'model_id')
    op.drop_column('cars_info', 'brand_id')
    # ### end Alembic commands ###
