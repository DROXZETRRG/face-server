"""Face service layer."""
from typing import List, Optional, Dict, Any, BinaryIO
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.face import Face
from app.schemas.face import FaceCreate
from app.core.storage import storage_manager


class FaceService:
    """Service for face operations."""
    
    @staticmethod
    def create(
        db: Session,
        face_data: FaceCreate,
        feature_vector: List[float],
        image_file: BinaryIO,
        filename: str
    ) -> Face:
        """Create a new face record.
        
        Args:
            db: Database session
            face_data: Face creation data
            feature_vector: Extracted feature vector
            image_file: Image file to store
            filename: Original filename
            
        Returns:
            Created face record
        """
        # Save image to storage
        image_url = storage_manager.save(image_file, filename, folder="faces")
        
        # Create face record
        face = Face(
            app_id=face_data.app_id,
            person_id=face_data.person_id,
            feature_vector=feature_vector,
            image_url=image_url,
            face_metadata=face_data.metadata
        )
        db.add(face)
        db.commit()
        db.refresh(face)
        return face
    
    @staticmethod
    def get_by_id(db: Session, face_id: UUID) -> Optional[Face]:
        """Get face by ID.
        
        Args:
            db: Database session
            face_id: Face ID
            
        Returns:
            Face if found, None otherwise
        """
        return db.query(Face).filter(
            and_(
                Face.id == face_id,
                Face.is_deleted == False
            )
        ).first()
    
    @staticmethod
    def list_by_app(
        db: Session,
        app_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Face], int]:
        """List faces by application with pagination.
        
        Args:
            db: Database session
            app_id: Application ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (faces list, total count)
        """
        query = db.query(Face).filter(
            and_(
                Face.app_id == app_id,
                Face.is_deleted == False
            )
        )
        total = query.count()
        faces = query.offset(skip).limit(limit).all()
        return faces, total
    
    @staticmethod
    def list_by_person(
        db: Session,
        app_id: UUID,
        person_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Face], int]:
        """List faces by person with pagination.
        
        Args:
            db: Database session
            app_id: Application ID
            person_id: Person ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (faces list, total count)
        """
        query = db.query(Face).filter(
            and_(
                Face.app_id == app_id,
                Face.person_id == person_id,
                Face.is_deleted == False
            )
        )
        total = query.count()
        faces = query.offset(skip).limit(limit).all()
        return faces, total
    
    @staticmethod
    def delete(db: Session, face_id: UUID) -> bool:
        """Soft delete a face record.
        
        Args:
            db: Database session
            face_id: Face ID
            
        Returns:
            True if deleted, False if not found
        """
        face = FaceService.get_by_id(db, face_id)
        if not face:
            return False
        
        face.is_deleted = True
        face.deleted_at = datetime.utcnow()
        db.commit()
        
        # Optionally delete the image file from storage
        # storage_manager.delete(face.image_url)
        
        return True
    
    @staticmethod
    def delete_by_person(db: Session, app_id: UUID, person_id: str) -> int:
        """Soft delete all faces of a person.
        
        Args:
            db: Database session
            app_id: Application ID
            person_id: Person ID
            
        Returns:
            Number of faces deleted
        """
        faces = db.query(Face).filter(
            and_(
                Face.app_id == app_id,
                Face.person_id == person_id,
                Face.is_deleted == False
            )
        ).all()
        
        count = 0
        for face in faces:
            face.is_deleted = True
            face.deleted_at = datetime.utcnow()
            count += 1
        
        db.commit()
        return count
