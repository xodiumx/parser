"""gcodes

Revision ID: a9be8456df5c
Revises: 1eaec2e10b3b
Create Date: 2023-09-18 09:55:14.782180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9be8456df5c'
down_revision = '1eaec2e10b3b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('leroy_products', sa.Column('gcode', sa.String(length=512), nullable=True))
    op.add_column('petrovich_analytics', sa.Column('vimos_gcode', sa.String(length=512), nullable=True))
    op.add_column('petrovich_products', sa.Column('gcode', sa.String(length=512), nullable=True))
    op.add_column('saturn_products', sa.Column('gcode', sa.String(length=512), nullable=True))
    op.add_column('stroyudacha_products', sa.Column('gcode', sa.String(length=512), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stroyudacha_products', 'gcode')
    op.drop_column('saturn_products', 'gcode')
    op.drop_column('petrovich_products', 'gcode')
    op.drop_column('petrovich_analytics', 'vimos_gcode')
    op.drop_column('leroy_products', 'gcode')
    # ### end Alembic commands ###
