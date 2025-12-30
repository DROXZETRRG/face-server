"""API response utilities."""
import uuid
from typing import Optional, Any
from app.schemas.common import ApiResponse


def generate_request_id() -> str:
    """生成唯一的请求ID."""
    return f"req_{uuid.uuid4().hex[:16]}"


def success_response(
    data: Any = None,
    message: str = "success",
    request_id: Optional[str] = None
) -> ApiResponse:
    """创建成功响应.
    
    Args:
        data: 响应数据
        message: 响应消息，默认 "success"
        request_id: 请求ID，如果不提供则自动生成
    
    Returns:
        统一格式的成功响应
    """
    if request_id is None:
        request_id = generate_request_id()
    
    return ApiResponse(
        code=0,
        message=message,
        data=data,
        request_id=request_id
    )


def error_response(
    code: int,
    message: str,
    data: Any = None,
    request_id: Optional[str] = None
) -> ApiResponse:
    """创建错误响应.
    
    Args:
        code: 错误码（非0）
        message: 错误消息
        data: 额外的错误信息
        request_id: 请求ID，如果不提供则自动生成
    
    Returns:
        统一格式的错误响应
    """
    if request_id is None:
        request_id = generate_request_id()
    
    return ApiResponse(
        code=code,
        message=message,
        data=data,
        request_id=request_id
    )


# 常用错误码定义
class ErrorCode:
    """错误码定义."""
    
    # 通用错误 (1xxx)
    INTERNAL_ERROR = 1000
    INVALID_PARAMETER = 1001
    RESOURCE_NOT_FOUND = 1004
    
    # 应用相关错误 (2xxx)
    APP_NOT_FOUND = 2001
    APP_CODE_EXISTS = 2002
    APP_CREATE_FAILED = 2003
    APP_UPDATE_FAILED = 2004
    APP_DELETE_FAILED = 2005
    
    # 人脸相关错误 (3xxx)
    FACE_NOT_FOUND = 3001
    FACE_NOT_DETECTED = 3002
    FACE_REGISTER_FAILED = 3003
    FACE_DELETE_FAILED = 3004
    FACE_SEARCH_FAILED = 3005
    INVALID_IMAGE = 3006
    INVALID_BASE64 = 3007
