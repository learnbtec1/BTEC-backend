"""add keitagorus foundation

Revision ID: a1b2c3d4e5f6
Revises: d98dd8ec85a3
Create Date: 2026-01-04 18:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'd98dd8ec85a3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create user_file table
    op.create_table(
        'userfile',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('owner_id', sa.Uuid(), nullable=False),
        sa.Column('original_filename', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('stored_path', sqlmodel.sql.sqltypes.AutoString(length=512), nullable=False),
        sa.Column('content_type', sqlmodel.sql.sqltypes.AutoString(length=128), nullable=False),
        sa.Column('size', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create student_progress table
    op.create_table(
        'studentprogress',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('lesson_id', sa.Uuid(), nullable=True),
        sa.Column('progress_percentage', sa.Integer(), nullable=False),
        sa.Column('last_score', sa.Float(), nullable=True),
        sa.Column('attempts', sa.Integer(), nullable=False),
        sa.Column('struggling', sa.Boolean(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add ar_model_url column to item table if it exists
    # This column can store URLs to AR/3D models for lessons
    try:
        op.add_column('item', sa.Column('ar_model_url', sqlmodel.sql.sqltypes.AutoString(length=512), nullable=True))
    except Exception:
        # Column might already exist or table might not exist
        pass


def downgrade() -> None:
    # Remove ar_model_url column from item table if it exists
    try:
        op.drop_column('item', 'ar_model_url')
    except Exception:
        pass
    
    # Drop student_progress table
    op.drop_table('studentprogress')
    
    # Drop user_file table
    op.drop_table('userfile')
