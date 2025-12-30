"""Configuration management using pydantic-settings."""
from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    database_url: str = "postgresql://faceserver:faceserver123@localhost:5432/faceserver"
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "faceserver"
    db_password: str = "faceserver123"
    db_name: str = "faceserver"
    
    # Storage
    storage_type: Literal["local", "oss", "s3"] = "local"
    local_storage_path: str = "./storage"
    
    # 阿里云 OSS 配置
    oss_access_key_id: str = ""
    oss_access_key_secret: str = ""
    oss_bucket_name: str = "face-server-bucket"
    oss_endpoint: str = "oss-cn-hangzhou.aliyuncs.com"  # 例如: oss-cn-hangzhou.aliyuncs.com
    oss_domain: str = ""  # 可选: 自定义域名，留空则使用默认域名
    
    # S3 兼容存储配置（保留向后兼容）
    cloud_storage_bucket: str = "face-server-bucket"
    cloud_storage_endpoint: str = "https://s3.amazonaws.com"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"
    
    # Face Recognition Engine
    face_model_pack: str = "buffalo_l"  # insightface 模型包: buffalo_l, buffalo_s, antelopev2
    face_det_size: tuple = (640, 640)  # 检测图像尺寸
    face_det_thresh: float = 0.5  # 检测置信度阈值
    face_device: str = "cpu"  # 设备: cpu, cuda
    face_ctx_id: int = -1  # GPU ID: -1 for CPU, 0+ for GPU
    face_model_dir: str = "~/.insightface"  # 模型目录
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
