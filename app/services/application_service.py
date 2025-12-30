"""Application service layer."""
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate


class ApplicationService:
    """Service for application operations."""
    
    @staticmethod
    def create(db: Session, app_data: ApplicationCreate) -> Application:
        """Create a new application.
        
        Args:
            db: Database session
            app_data: Application creation data
            
        Returns:
            Created application
        """
        app = Application(
            app_code=app_data.app_code,
            app_name=app_data.app_name
        )
        db.add(app)
        db.commit()
        db.refresh(app)
        return app
    
    @staticmethod
    def get_by_id(db: Session, app_id: UUID) -> Optional[Application]:
        """Get application by ID.
        
        Args:
            db: Database session
            app_id: Application ID
            
        Returns:
            Application if found, None otherwise
        """
        return db.query(Application).filter(
            and_(
                Application.id == app_id,
                Application.is_deleted == False
            )
        ).first()
    
    @staticmethod
    def get_by_code(db: Session, app_code: str) -> Optional[Application]:
        """Get application by code.
        
        Args:
            db: Database session
            app_code: Application code
            
        Returns:
            Application if found, None otherwise
        """
        return db.query(Application).filter(
            and_(
                Application.app_code == app_code,
                Application.is_deleted == False
            )
        ).first()
    
    @staticmethod
    def list_all(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Application], int]:
        """List all applications with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (applications list, total count)
        """
        query = db.query(Application).filter(Application.is_deleted == False)
        total = query.count()
        apps = query.offset(skip).limit(limit).all()
        return apps, total
    
    @staticmethod
    def update(
        db: Session,
        app_id: UUID,
        app_data: ApplicationUpdate
    ) -> Optional[Application]:
        """Update an application.
        
        Args:
            db: Database session
            app_id: Application ID
            app_data: Update data
            
        Returns:
            Updated application if found, None otherwise
        """
        app = ApplicationService.get_by_id(db, app_id)
        if not app:
            return None
        
        if app_data.app_name is not None:
            app.app_name = app_data.app_name
        
        app.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(app)
        return app
    
    @staticmethod
    def delete(db: Session, app_id: UUID) -> bool:
        """Soft delete an application.
        
        Args:
            db: Database session
            app_id: Application ID
            
        Returns:
            True if deleted, False if not found
        """
        app = ApplicationService.get_by_id(db, app_id)
        if not app:
            return False
        
        app.is_deleted = True
        app.deleted_at = datetime.utcnow()
        db.commit()
        return True
