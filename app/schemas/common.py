"""Common schemas."""
from typing import Optional, Any, Generic, TypeVar
from pydantic import BaseModel, Field

# 泛型类型变量
T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """统一的 API 响应格式.
    
    所有 API 接口统一返回此格式:
    - HTTP 状态码始终为 200
    - 通过 code 字段区分成功/失败
    - code = 0 表示成功，其他值表示错误
    """
    code: int = Field(..., description="响应码，0表示成功，其他值表示错误")
    message: str = Field(..., description="响应消息")
    data: Optional[T] = Field(None, description="响应数据")
    request_id: str = Field(..., description="请求追踪ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": 0,
                "message": "success",
                "data": {},
                "request_id": "req_123456789"
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    message: str


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: str
