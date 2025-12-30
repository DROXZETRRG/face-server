"""Application model."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Application(Base):
    """Application table model."""
    
    __tablename__ = "applications"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Application fields
    app_code = Column(String(100), unique=True, nullable=False, index=True)
    app_name = Column(String(200), nullable=False)
    
    # Common fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    
    # Relationships
    faces = relationship("Face", back_populates="application")
