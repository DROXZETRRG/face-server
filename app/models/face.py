"""Face model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.database import Base


class Face(Base):
    """Face table model."""
    
    __tablename__ = "faces"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign keys
    app_id = Column(UUID(as_uuid=True), ForeignKey("applications.id"), nullable=False, index=True)
    
    # Face fields
    person_id = Column(String(100), nullable=False, index=True)
    feature_vector = Column(Vector(512), nullable=False)  # 512-dimensional feature vector
    image_url = Column(String(500), nullable=False)
    face_metadata = Column(JSONB, nullable=True)  # Additional metadata with GIN index
    
    # Common fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    
    # Relationships
    application = relationship("Application", back_populates="faces")
    
    # Indexes
    __table_args__ = (
        Index("ix_faces_face_metadata_gin", "face_metadata", postgresql_using="gin"),
    )
