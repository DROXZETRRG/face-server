"""Rename metadata to face_metadata

Revision ID: 002
Revises: 001
Create Date: 2025-12-30 00:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rename column metadata to face_metadata
    op.alter_column('faces', 'metadata', new_column_name='face_metadata')
    
    # Drop old index and create new one with correct column name
    op.drop_index('ix_faces_metadata_gin', table_name='faces')
    op.create_index('ix_faces_face_metadata_gin', 'faces', ['face_metadata'], postgresql_using='gin')


def downgrade() -> None:
    # Revert: rename face_metadata back to metadata
    op.drop_index('ix_faces_face_metadata_gin', table_name='faces')
    op.create_index('ix_faces_metadata_gin', 'faces', ['metadata'], postgresql_using='gin')
    op.alter_column('faces', 'face_metadata', new_column_name='metadata')
