"""Add AR support and StudentProgress table

Revision ID: a1b2c3d4e5f6
Revises: 1a31ce608336
Create Date: 2026-01-03 17:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '1a31ce608336'
branch_labels = None
depends_on = None


def upgrade():
    # Add ar_model_url column to item table
    op.add_column('item', sa.Column('ar_model_url', sa.VARCHAR(length=2048), nullable=True))
    
    # Create studentprogress table
    op.create_table(
        'studentprogress',
        sa.Column('module_name', sa.VARCHAR(length=255), nullable=False),
        sa.Column('progress', sa.Integer(), nullable=False),
        sa.Column('struggling', sa.Boolean(), nullable=False),
        sa.Column('last_score', sa.Float(), nullable=True),
        sa.Column('attempts', sa.Integer(), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Drop studentprogress table
    op.drop_table('studentprogress')
    
    # Remove ar_model_url column from item table
    op.drop_column('item', 'ar_model_url')
