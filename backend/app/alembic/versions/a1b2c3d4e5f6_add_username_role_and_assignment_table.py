"""Add username role to User and create Assignment table

Revision ID: a1b2c3d4e5f6
Revises: 1a31ce608336
Create Date: 2026-01-02 20:00:00.000000

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
    # Add username and role columns to user table
    op.add_column('user', sa.Column('username', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=True))
    op.add_column('user', sa.Column('role', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False, server_default='student'))
    
    # Create unique index on username
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    
    # Update existing users to have a username (use email prefix as username)
    op.execute("""
        UPDATE "user" 
        SET username = SPLIT_PART(email, '@', 1) 
        WHERE username IS NULL
    """)
    
    # Make username non-nullable after populating
    op.alter_column('user', 'username', nullable=False)
    
    # Create assignment table
    op.create_table(
        'assignment',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=1000), nullable=True),
        sa.Column('student_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('teacher_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('file_path', sqlmodel.sql.sqltypes.AutoString(length=500), nullable=False),
        sa.Column('file_name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), nullable=False),
        sa.Column('graded_at', sa.DateTime(), nullable=True),
        sa.Column('grade', sa.Float(), nullable=True),
        sa.Column('status', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False, server_default='pending'),
        sa.Column('comments', sqlmodel.sql.sqltypes.AutoString(length=1000), nullable=True),
        sa.ForeignKeyConstraint(['student_id'], ['user.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['teacher_id'], ['user.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Drop assignment table
    op.drop_table('assignment')
    
    # Drop username index and column from user table
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_column('user', 'role')
    op.drop_column('user', 'username')
