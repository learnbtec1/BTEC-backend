"""Add StudentProgress table and ar_model_url to Item

Revision ID: a1b2c3d4e5f6
Revises: 1a31ce608336
Create Date: 2026-01-03 19:03:00.000000

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
    op.add_column('item', sa.Column('ar_model_url', sa.String(length=512), nullable=True))

    # Create studentprogress table
    op.create_table('studentprogress',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('subject', sa.String(length=255), nullable=False),
        sa.Column('topic', sa.String(length=255), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('notes', sa.String(length=1000), nullable=True),
        sa.Column('student_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['student_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Drop studentprogress table
    op.drop_table('studentprogress')
    
    # Drop ar_model_url column from item table
    op.drop_column('item', 'ar_model_url')
