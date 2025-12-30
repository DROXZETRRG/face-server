"""Initial migration - create applications and faces tables

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector
import uuid

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    
    # Create applications table
    op.create_table(
        'applications',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('app_code', sa.String(100), nullable=False, unique=True),
        sa.Column('app_name', sa.String(200), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
    )
    
    # Create indexes for applications
    op.create_index('ix_applications_id', 'applications', ['id'])
    op.create_index('ix_applications_app_code', 'applications', ['app_code'])
    op.create_index('ix_applications_is_deleted', 'applications', ['is_deleted'])
    
    # Create faces table
    op.create_table(
        'faces',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('app_id', UUID(as_uuid=True), nullable=False),
        sa.Column('person_id', sa.String(100), nullable=False),
        sa.Column('feature_vector', Vector(512), nullable=False),
        sa.Column('image_url', sa.String(500), nullable=False),
        sa.Column('metadata', JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.ForeignKeyConstraint(['app_id'], ['applications.id'], ),
    )
    
    # Create indexes for faces
    op.create_index('ix_faces_id', 'faces', ['id'])
    op.create_index('ix_faces_app_id', 'faces', ['app_id'])
    op.create_index('ix_faces_person_id', 'faces', ['person_id'])
    op.create_index('ix_faces_is_deleted', 'faces', ['is_deleted'])
    op.create_index('ix_faces_metadata_gin', 'faces', ['metadata'], postgresql_using='gin')


def downgrade() -> None:
    # Drop faces table
    op.drop_index('ix_faces_metadata_gin', table_name='faces')
    op.drop_index('ix_faces_is_deleted', table_name='faces')
    op.drop_index('ix_faces_person_id', table_name='faces')
    op.drop_index('ix_faces_app_id', table_name='faces')
    op.drop_index('ix_faces_id', table_name='faces')
    op.drop_table('faces')
    
    # Drop applications table
    op.drop_index('ix_applications_is_deleted', table_name='applications')
    op.drop_index('ix_applications_app_code', table_name='applications')
    op.drop_index('ix_applications_id', table_name='applications')
    op.drop_table('applications')
    
    # Drop pgvector extension
    op.execute('DROP EXTENSION IF EXISTS vector')
