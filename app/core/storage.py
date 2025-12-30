"""Storage module for file management.

This module provides unified interface for file storage,
supporting both local file system and cloud storage.
"""
from typing import BinaryIO, Optional
from pathlib import Path
from abc import ABC, abstractmethod
import os
import uuid
import logging
from app.config import settings

try:
    import oss2
    OSS_AVAILABLE = True
except ImportError:
    OSS_AVAILABLE = False

logger = logging.getLogger(__name__)


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


class OSSStorage(StorageBackend):
    """阿里云 OSS 存储后端。"""
    
    def __init__(
        self,
        access_key_id: str = None,
        access_key_secret: str = None,
        bucket_name: str = None,
        endpoint: str = None,
        domain: str = None
    ):
        """初始化阿里云 OSS 存储。
        
        Args:
            access_key_id: 阿里云 AccessKey ID
            access_key_secret: 阿里云 AccessKey Secret
            bucket_name: OSS bucket 名称
            endpoint: OSS endpoint (例如: oss-cn-hangzhou.aliyuncs.com)
            domain: 自定义域名（可选）
        """
        if not OSS_AVAILABLE:
            raise ImportError(
                "oss2 is not installed. Install it with: pip install oss2"
            )
        
        self.access_key_id = access_key_id or settings.oss_access_key_id
        self.access_key_secret = access_key_secret or settings.oss_access_key_secret
        self.bucket_name = bucket_name or settings.oss_bucket_name
        self.endpoint = endpoint or settings.oss_endpoint
        self.domain = domain or settings.oss_domain
        
        if not self.access_key_id or not self.access_key_secret:
            raise ValueError(
                "OSS credentials are required. Set OSS_ACCESS_KEY_ID and "
                "OSS_ACCESS_KEY_SECRET in environment variables or .env file"
            )
        
        # 初始化 OSS 认证和 Bucket
        auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        self.bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
        
        logger.info(
            f"Initialized OSS storage: bucket={self.bucket_name}, "
            f"endpoint={self.endpoint}"
        )
    
    def save(self, file: BinaryIO, filename: str, folder: str = "") -> str:
        """保存文件到阿里云 OSS。
        
        Args:
            file: 文件对象
            filename: 原始文件名
            folder: 可选的文件夹前缀
            
        Returns:
            对象 key（用于访问文件）
        """
        # 生成唯一文件名
        ext = os.path.splitext(filename)[1]
        unique_filename = f"{uuid.uuid4()}{ext}"
        
        # 构建对象 key
        if folder:
            object_key = f"{folder}/{unique_filename}"
        else:
            object_key = unique_filename
        
        # 上传文件
        try:
            file_data = file.read()
            result = self.bucket.put_object(object_key, file_data)
            
            if result.status == 200:
                logger.info(f"File uploaded to OSS: {object_key}")
                return object_key
            else:
                raise Exception(f"OSS upload failed with status: {result.status}")
        except Exception as e:
            logger.error(f"Failed to upload file to OSS: {e}")
            raise
    
    def delete(self, file_path: str) -> bool:
        """从阿里云 OSS 删除文件。
        
        Args:
            file_path: 对象 key
            
        Returns:
            是否删除成功
        """
        try:
            result = self.bucket.delete_object(file_path)
            if result.status == 204:
                logger.info(f"File deleted from OSS: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete file from OSS: {e}")
            return False
    
    def exists(self, file_path: str) -> bool:
        """检查文件是否存在于阿里云 OSS。
        
        Args:
            file_path: 对象 key
            
        Returns:
            文件是否存在
        """
        try:
            return self.bucket.object_exists(file_path)
        except Exception as e:
            logger.error(f"Failed to check file existence in OSS: {e}")
            return False
    
    def get_url(self, file_path: str) -> str:
        """获取文件的访问 URL。
        
        Args:
            file_path: 对象 key
            
        Returns:
            文件的公网访问 URL
        """
        if self.domain:
            # 使用自定义域名
            return f"https://{self.domain}/{file_path}"
        else:
            # 使用默认 OSS 域名
            return f"https://{self.bucket_name}.{self.endpoint}/{file_path}"


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
        elif settings.storage_type == "oss":
            self.backend = OSSStorage()
        elif settings.storage_type == "s3":
            self.backend = CloudStorage()
        else:
            logger.warning(
                f"Unknown storage type: {settings.storage_type}, "
                "falling back to local storage"
            )
            self.backend = LocalStorage()
    
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
