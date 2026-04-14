"""create products table

Revision ID: 001_create_products
Revises: 
Create Date: 2025-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '001_create_products'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('count', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)

    op.execute("INSERT INTO products (title, price, count) VALUES ('Laptop', 999.99, 10)")
    op.execute("INSERT INTO products (title, price, count) VALUES ('Mouse', 29.99, 50)")


def downgrade() -> None:
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
