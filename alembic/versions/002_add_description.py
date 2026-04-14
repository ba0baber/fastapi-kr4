"""add description to products

Revision ID: 002_add_description
Revises: 001_create_products
Create Date: 2025-01-01 00:01:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '002_add_description'
down_revision = '001_create_products'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('products', sa.Column('description', sa.Text(), nullable=True))
    op.execute("UPDATE products SET description = 'No description' WHERE description IS NULL")
    op.alter_column('products', 'description', nullable=False)


def downgrade() -> None:
    op.drop_column('products', 'description')
