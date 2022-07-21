"""added model of the car

Revision ID: 51781f18df06
Revises: 
Create Date: 2022-03-07 19:14:46.977312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51781f18df06'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cars_info',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('auto_id', sa.Integer(), nullable=True),
    sa.Column('race', sa.Integer(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('fuel_name', sa.String(), nullable=True),
    sa.Column('fuel_value', sa.Integer(), nullable=True),
    sa.Column('gear_box_auto', sa.Boolean(), nullable=True),
    sa.Column('has_damage', sa.Boolean(), nullable=True),
    sa.Column('link', sa.String(), nullable=True),
    sa.Column('vin', sa.String(), nullable=True),
    sa.Column('parsed_from', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('auto_id'),
    sa.UniqueConstraint('link')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cars_info')
    # ### end Alembic commands ###
