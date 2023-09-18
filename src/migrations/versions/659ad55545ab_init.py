"""init

Revision ID: 659ad55545ab
Revises: 
Create Date: 2023-08-29 15:37:56.686731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '659ad55545ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('petrovich_products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=512), nullable=True),
    sa.Column('price', sa.Numeric(decimal_return_scale=1), nullable=True),
    sa.Column('cart_price', sa.Numeric(decimal_return_scale=1), nullable=True),
    sa.Column('currency', sa.String(length=10), nullable=True),
    sa.Column('url', sa.String(length=512), nullable=True),
    sa.Column('created_at', sa.Date(), nullable=True),
    sa.Column('measurement', sa.String(length=64), nullable=True),
    sa.Column('category', sa.String(length=128), nullable=True),
    sa.Column('exists', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_petrovich_products_id'), 'petrovich_products', ['id'], unique=False)
    op.create_table('saturn_products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=512), nullable=True),
    sa.Column('price', sa.Numeric(decimal_return_scale=1), nullable=True),
    sa.Column('cart_price', sa.Numeric(decimal_return_scale=1), nullable=True),
    sa.Column('currency', sa.String(length=10), nullable=True),
    sa.Column('url', sa.String(length=512), nullable=True),
    sa.Column('created_at', sa.Date(), nullable=True),
    sa.Column('measurement', sa.String(length=64), nullable=True),
    sa.Column('category', sa.String(length=128), nullable=True),
    sa.Column('exists', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_saturn_products_id'), 'saturn_products', ['id'], unique=False)
    op.create_table('stroyudacha_products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=512), nullable=True),
    sa.Column('price', sa.Numeric(decimal_return_scale=1), nullable=True),
    sa.Column('cart_price', sa.Numeric(decimal_return_scale=1), nullable=True),
    sa.Column('currency', sa.String(length=10), nullable=True),
    sa.Column('url', sa.String(length=512), nullable=True),
    sa.Column('created_at', sa.Date(), nullable=True),
    sa.Column('measurement', sa.String(length=64), nullable=True),
    sa.Column('category', sa.String(length=128), nullable=True),
    sa.Column('exists', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stroyudacha_products_id'), 'stroyudacha_products', ['id'], unique=False)
    op.create_table('vimos_products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=512), nullable=True),
    sa.Column('price', sa.DECIMAL(), nullable=True),
    sa.Column('currency', sa.String(length=10), nullable=True),
    sa.Column('url', sa.String(length=512), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vimos_products_id'), 'vimos_products', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_vimos_products_id'), table_name='vimos_products')
    op.drop_table('vimos_products')
    op.drop_index(op.f('ix_stroyudacha_products_id'), table_name='stroyudacha_products')
    op.drop_table('stroyudacha_products')
    op.drop_index(op.f('ix_saturn_products_id'), table_name='saturn_products')
    op.drop_table('saturn_products')
    op.drop_index(op.f('ix_petrovich_products_id'), table_name='petrovich_products')
    op.drop_table('petrovich_products')
    # ### end Alembic commands ###