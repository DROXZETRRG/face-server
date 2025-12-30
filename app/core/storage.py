"""Storage module for file management.

This module provides unified interface for file storage,
supporting both local file system and cloud storage.
"""
from typing import BinaryIO, Optional
from pathlib import Path
from abc import ABC, abstractmethod
import os
import uuid
from app.config import settings


class StorageBackend(ABC):
    """Abstract base class for storage backends."""
    
    @abstractmethod
    def save(self, file: BinaryIO, filename: str, folder: str = "") -> str:
        """Save a file and return its URL/path.
        
        Args:
            file: File-like object to save
            filename: Original filename
            folder: Optional folder/prefix for organization
            
        Returns:
            URL or path to the saved file
        """
        pass
    
    @abstractmethod
    def delete(self, file_path: str) -> bool:
        """Delete a file.
        
        Args:
            file_path: Path or URL of the file to delete
            
        Returns:
            True if deletion was successful
        """
        pass
    
    @abstractmethod
    def exists(self, file_path: str) -> bool:
        """Check if a file exists.
        
        Args:
            file_path: Path or URL of the file
            
        Returns:
            True if file exists
        """
        pass
    
    @abstractmethod
    def get_url(self, file_path: str) -> str:
        """Get the accessible URL for a file.
        
        Args:
            file_path: Internal file path
            
        Returns:
            Public URL to access the file
        """
        pass


class LocalStorage(StorageBackend):
    """Local file system storage backend."""
    
    def __init__(self, base_path: str = None):
        """Initialize local storage.
        
        Args:
            base_path: Base directory for file storage
        """
        self.base_path = Path(base_path or settings.local_storage_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def save(self, file: BinaryIO, filename: str, folder: str = "") -> str:
        """Save a file to local storage.
        
        Args:
            file: File-like object to save
            filename: Original filename
            folder: Optional subfolder
            
        Returns:
            Relative path to the saved file
        """
        # Generate unique filename
        ext = os.path.splitext(filename)[1]
        unique_filename = f"{uuid.uuid4()}{ext}"
        
        # Create folder if specified
        if folder:
            save_dir = self.base_path / folder
            save_dir.mkdir(parents=True, exist_ok=True)
            file_path = save_dir / unique_filename
            relative_path = f"{folder}/{unique_filename}"
        else:
            file_path = self.base_path / unique_filename
            relative_path = unique_filename
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(file.read())
        
        return relative_path
    
    def delete(self, file_path: str) -> bool:
        """Delete a file from local storage.
        
        Args:
            file_path: Relative path to the file
            
        Returns:
            True if deletion was successful
        """
        try:
            full_path = self.base_path / file_path
            if full_path.exists():
                full_path.unlink()
                return True
            return False
        except Exception:
            return False
    
    def exists(self, file_path: str) -> bool:
        """Check if a file exists in local storage.
        
        Args:
            file_path: Relative path to the file
            
        Returns:
            True if file exists
        """
        full_path = self.base_path / file_path
        return full_path.exists()
    
    def get_url(self, file_path: str) -> str:
        """Get the URL for a file (for local storage, returns the path).
        
        Args:
            file_path: Relative path to the file
            
        Returns:
            File path or URL
        """
        return f"/storage/{file_path}"


class CloudStorage(StorageBackend):
    """Cloud storage backend (S3-compatible).
    
    This is a placeholder implementation. In production, you would
    use boto3 or similar library to interact with cloud storage.
    """
    
    def __init__(
        self,
        bucket: str = None,
        endpoint: str = None,
        access_key: str = None,
        secret_key: str = None
    ):
        """Initialize cloud storage.
        
        Args:
            bucket: Storage bucket name
            endpoint: Storage endpoint URL
            access_key: Access key for authentication
            secret_key: Secret key for authentication
        """
        self.bucket = bucket or settings.cloud_storage_bucket
        self.endpoint = endpoint or settings.cloud_storage_endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self._client = None
    
    def _get_client(self):
        """Get or create storage client.
        
        Returns:
            Storage client instance
        """
        # Placeholder - in production, initialize boto3 client here
        pass
    
    def save(self, file: BinaryIO, filename: str, folder: str = "") -> str:
        """Save a file to cloud storage.
        
        Args:
            file: File-like object to save
            filename: Original filename
            folder: Optional folder/prefix
            
        Returns:
            Object key or URL
        """
        # Placeholder implementation
        pass
    
    def delete(self, file_path: str) -> bool:
        """Delete a file from cloud storage.
        
        Args:
            file_path: Object key
            
        Returns:
            True if deletion was successful
        """
        # Placeholder implementation
        pass
    
    def exists(self, file_path: str) -> bool:
        """Check if a file exists in cloud storage.
        
        Args:
            file_path: Object key
            
        Returns:
            True if file exists
        """
        # Placeholder implementation
        pass
    
    def get_url(self, file_path: str) -> str:
        """Get the public URL for a file.
        
        Args:
            file_path: Object key
            
        Returns:
            Public URL
        """
        # Placeholder implementation
        return f"{self.endpoint}/{self.bucket}/{file_path}"


class StorageManager:
    """Storage manager that provides unified interface."""
    
    def __init__(self, backend: Optional[StorageBackend] = None):
        """Initialize storage manager.
        
        Args:
            backend: Storage backend to use. If None, uses default from settings.
        """
        if backend:
            self.backend = backend
        elif settings.storage_type == "local":
            self.backend = LocalStorage()
        else:
            self.backend = CloudStorage()
    
    def save(self, file: BinaryIO, filename: str, folder: str = "") -> str:
        """Save a file using the configured backend."""
        return self.backend.save(file, filename, folder)
    
    def delete(self, file_path: str) -> bool:
        """Delete a file using the configured backend."""
        return self.backend.delete(file_path)
    
    def exists(self, file_path: str) -> bool:
        """Check if a file exists using the configured backend."""
        return self.backend.exists(file_path)
    
    def get_url(self, file_path: str) -> str:
        """Get file URL using the configured backend."""
        return self.backend.get_url(file_path)


# Global storage manager instance
storage_manager = StorageManager()
