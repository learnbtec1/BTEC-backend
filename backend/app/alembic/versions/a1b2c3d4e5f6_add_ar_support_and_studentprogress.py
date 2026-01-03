"""Add AR support and StudentProgress table

Revision ID: a1b2c3d4e5f6
Revises: d98dd8ec85a3
Create Date: 2026-01-03 09:35:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'd98dd8ec85a3'
branch_labels = None
depends_on = None


def upgrade():
    # Add ar_model_url column to item table
    op.add_column(
        'item',
        sa.Column('ar_model_url', sa.String(length=2048), nullable=True)
    )

    # Create studentprogress table
    op.create_table(
        'studentprogress',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('module_name', sa.String(length=255), nullable=False),
        sa.Column('progress_percentage', sa.Integer(), nullable=False),
        sa.Column('struggling', sa.Boolean(), nullable=False),
        sa.Column('last_activity', sa.String(length=255), nullable=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Drop studentprogress table
    op.drop_table('studentprogress')

    # Remove ar_model_url column from item table
    op.drop_column('item', 'ar_model_url')
