# 统一响应格式说明

## 概述

所有 API 接口统一返回格式：

- ✅ **HTTP 状态码**: 始终返回 **200 OK**
- ✅ **响应格式**: 统一的 JSON 结构
- ✅ **成功标识**: 通过 `code` 字段区分成功/失败
- ✅ **请求追踪**: 每个响应包含唯一的 `request_id`

## 响应格式

### 基本结构

```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "request_id": "req_a1b2c3d4e5f6g7h8"
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 响应码，0表示成功，其他值表示错误 |
| message | string | 响应消息，成功时为"success"或操作描述，失败时为错误描述 |
| data | any | 响应数据，成功时包含业务数据，失败时可能为null或包含错误详情 |
| request_id | string | 请求追踪ID，格式为"req_"开头的16位随机字符串 |

## 错误码定义

### 通用错误 (1xxx)

| 错误码 | 说明 |
|--------|------|
| 1000 | 内部服务器错误 |
| 1001 | 无效的参数 |
| 1004 | 资源不存在 |

### 应用相关错误 (2xxx)

| 错误码 | 说明 |
|--------|------|
| 2001 | 应用不存在 |
| 2002 | 应用代码已存在 |
| 2003 | 应用创建失败 |
| 2004 | 应用更新失败 |
| 2005 | 应用删除失败 |

### 人脸相关错误 (3xxx)

| 错误码 | 说明 |
|--------|------|
| 3001 | 人脸不存在 |
| 3002 | 未检测到人脸 |
| 3003 | 人脸注册失败 |
| 3004 | 人脸删除失败 |
| 3005 | 人脸搜索失败 |
| 3006 | 无效的图像 |
| 3007 | 无效的Base64编码 |

## 响应示例

### 1. 成功响应 - 创建应用

**请求**:
```bash
curl -X POST "http://localhost:8000/api/v1/applications/create" \
  -H "Content-Type: application/json" \
  -d '{
    "app_code": "my_app",
    "app_name": "我的应用"
  }'
```

**响应** (HTTP 200):
```json
{
  "code": 0,
  "message": "Application created successfully",
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "app_code": "my_app",
    "app_name": "我的应用",
    "created_at": "2025-12-30T10:00:00Z",
    "updated_at": "2025-12-30T10:00:00Z"
  },
  "request_id": "req_a1b2c3d4e5f6g7h8"
}
```

---

### 2. 成功响应 - 查询列表

**请求**:
```bash
curl -X POST "http://localhost:8000/api/v1/applications/list" \
  -H "Content-Type: application/json" \
  -d '{
    "skip": 0,
    "limit": 10
  }'
```

**响应** (HTTP 200):
```json
{
  "code": 0,
  "message": "Applications retrieved successfully",
  "data": {
    "total": 5,
    "items": [
      {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "app_code": "my_app",
        "app_name": "我的应用",
        "created_at": "2025-12-30T10:00:00Z",
        "updated_at": "2025-12-30T10:00:00Z"
      }
    ]
  },
  "request_id": "req_b2c3d4e5f6g7h8i9"
}
```

---

### 3. 成功响应 - 删除操作

**请求**:
```bash
curl -X POST "http://localhost:8000/api/v1/applications/delete" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "123e4567-e89b-12d3-a456-426614174000"
  }'
```

**响应** (HTTP 200):
```json
{
  "code": 0,
  "message": "Application deleted successfully",
  "data": null,
  "request_id": "req_c3d4e5f6g7h8i9j0"
}
```

---

### 4. 错误响应 - 资源不存在

**请求**:
```bash
curl -X POST "http://localhost:8000/api/v1/applications/get" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "non-existent-id"
  }'
```

**响应** (HTTP 200):
```json
{
  "code": 2001,
  "message": "Application with ID 'non-existent-id' not found",
  "data": null,
  "request_id": "req_d4e5f6g7h8i9j0k1"
}
```

---

### 5. 错误响应 - 应用代码重复

**请求**:
```bash
curl -X POST "http://localhost:8000/api/v1/applications/create" \
  -H "Content-Type: application/json" \
  -d '{
    "app_code": "existing_app",
    "app_name": "测试"
  }'
```

**响应** (HTTP 200):
```json
{
  "code": 2002,
  "message": "Application with code 'existing_app' already exists",
  "data": null,
  "request_id": "req_e5f6g7h8i9j0k1l2"
}
```

---

### 6. 成功响应 - 注册人脸

**请求**:
```bash
IMAGE_BASE64=$(base64 -w 0 face.jpg)

curl -X POST "http://localhost:8000/api/v1/faces/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"app_id\": \"123e4567-e89b-12d3-a456-426614174000\",
    \"person_id\": \"person_001\",
    \"image_base64\": \"$IMAGE_BASE64\",
    \"metadata\": {
      \"name\": \"张三\",
      \"department\": \"技术部\"
    }
  }"
```

**响应** (HTTP 200):
```json
{
  "code": 0,
  "message": "Face registered successfully",
  "data": {
    "id": "face-uuid",
    "app_id": "123e4567-e89b-12d3-a456-426614174000",
    "person_id": "person_001",
    "image_url": "http://storage.example.com/faces/abc123.jpg",
    "metadata": {
      "name": "张三",
      "department": "技术部"
    },
    "created_at": "2025-12-30T10:00:00Z",
    "updated_at": "2025-12-30T10:00:00Z"
  },
  "request_id": "req_f6g7h8i9j0k1l2m3"
}
```

---

### 7. 错误响应 - 未检测到人脸

**请求**:
```bash
IMAGE_BASE64=$(base64 -w 0 no_face.jpg)

curl -X POST "http://localhost:8000/api/v1/faces/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"app_id\": \"123e4567-e89b-12d3-a456-426614174000\",
    \"person_id\": \"person_002\",
    \"image_base64\": \"$IMAGE_BASE64\"
  }"
```

**响应** (HTTP 200):
```json
{
  "code": 3002,
  "message": "No face detected in the image",
  "data": null,
  "request_id": "req_g7h8i9j0k1l2m3n4"
}
```

---

### 8. 成功响应 - 搜索人脸

**请求**:
```bash
IMAGE_BASE64=$(base64 -w 0 query.jpg)

curl -X POST "http://localhost:8000/api/v1/faces/search" \
  -H "Content-Type: application/json" \
  -d "{
    \"app_id\": \"123e4567-e89b-12d3-a456-426614174000\",
    \"image_base64\": \"$IMAGE_BASE64\",
    \"top_k\": 5,
    \"threshold\": 0.7
  }"
```

**响应** (HTTP 200):
```json
{
  "code": 0,
  "message": "Face search completed successfully",
  "data": {
    "query_time_ms": 45.2,
    "results": [
      {
        "face_id": "face-uuid-1",
        "person_id": "person_001",
        "similarity": 0.95,
        "image_url": "http://storage.example.com/faces/abc123.jpg",
        "metadata": {
          "name": "张三",
          "department": "技术部"
        }
      },
      {
        "face_id": "face-uuid-2",
        "person_id": "person_002",
        "similarity": 0.87,
        "image_url": "http://storage.example.com/faces/def456.jpg",
        "metadata": {
          "name": "李四",
          "department": "技术部"
        }
      }
    ]
  },
  "request_id": "req_h8i9j0k1l2m3n4o5"
}
```

---

### 9. 错误响应 - Base64 解码失败

**请求**:
```bash
curl -X POST "http://localhost:8000/api/v1/faces/register" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "123e4567-e89b-12d3-a456-426614174000",
    "person_id": "person_003",
    "image_base64": "invalid_base64_string!!!"
  }'
```

**响应** (HTTP 200):
```json
{
  "code": 3007,
  "message": "Invalid base64 image data: Invalid base64-encoded string",
  "data": null,
  "request_id": "req_i9j0k1l2m3n4o5p6"
}
```

## Python 客户端示例

### 基础客户端封装

```python
import base64
import requests
from typing import Optional, Dict, Any


class FaceAPIClient:
    """人脸识别 API 客户端."""
    
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
    
    def _request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """发送请求并处理响应.
        
        Args:
            endpoint: API 端点
            data: 请求数据
        
        Returns:
            API 响应
        
        Raises:
            Exception: 当 API 返回错误时
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data)
        
        # HTTP 状态码始终是 200
        if response.status_code != 200:
            raise Exception(f"HTTP error: {response.status_code}")
        
        result = response.json()
        
        # 检查业务错误码
        if result['code'] != 0:
            raise Exception(
                f"API error {result['code']}: {result['message']} "
                f"(request_id: {result['request_id']})"
            )
        
        return result
    
    # 应用管理
    def create_application(self, app_code: str, app_name: str) -> Dict[str, Any]:
        """创建应用."""
        result = self._request("/applications/create", {
            "app_code": app_code,
            "app_name": app_name
        })
        return result['data']
    
    def list_applications(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """查询应用列表."""
        result = self._request("/applications/list", {
            "skip": skip,
            "limit": limit
        })
        return result['data']
    
    def get_application(self, app_id: str) -> Dict[str, Any]:
        """获取应用详情."""
        result = self._request("/applications/get", {
            "app_id": app_id
        })
        return result['data']
    
    def update_application(self, app_id: str, app_name: str) -> Dict[str, Any]:
        """更新应用."""
        result = self._request("/applications/update", {
            "app_id": app_id,
            "app_name": app_name
        })
        return result['data']
    
    def delete_application(self, app_id: str) -> None:
        """删除应用."""
        self._request("/applications/delete", {"app_id": app_id})
    
    # 人脸管理
    def register_face(
        self,
        app_id: str,
        person_id: str,
        image_path: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """注册人脸."""
        with open(image_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode()
        
        data = {
            "app_id": app_id,
            "person_id": person_id,
            "image_base64": image_base64
        }
        if metadata:
            data["metadata"] = metadata
        
        result = self._request("/faces/register", data)
        return result['data']
    
    def list_faces(
        self,
        app_id: str,
        person_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """查询人脸列表."""
        data = {
            "app_id": app_id,
            "skip": skip,
            "limit": limit
        }
        if person_id:
            data["person_id"] = person_id
        
        result = self._request("/faces/list", data)
        return result['data']
    
    def get_face(self, face_id: str) -> Dict[str, Any]:
        """获取人脸详情."""
        result = self._request("/faces/get", {"face_id": face_id})
        return result['data']
    
    def delete_face(self, face_id: str) -> None:
        """删除人脸."""
        self._request("/faces/delete", {"face_id": face_id})
    
    def search_faces(
        self,
        app_id: str,
        image_path: str,
        top_k: int = 10,
        threshold: float = 0.6,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """搜索人脸."""
        with open(image_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode()
        
        data = {
            "app_id": app_id,
            "image_base64": image_base64,
            "top_k": top_k,
            "threshold": threshold
        }
        if metadata_filter:
            data["metadata_filter"] = metadata_filter
        
        result = self._request("/faces/search", data)
        return result['data']


# 使用示例
if __name__ == "__main__":
    client = FaceAPIClient()
    
    try:
        # 创建应用
        app = client.create_application("test_app", "测试应用")
        print(f"✅ Created app: {app['id']}")
        
        # 注册人脸
        face = client.register_face(
            app_id=app['id'],
            person_id="person_001",
            image_path="face.jpg",
            metadata={"name": "张三"}
        )
        print(f"✅ Registered face: {face['id']}")
        
        # 搜索人脸
        results = client.search_faces(
            app_id=app['id'],
            image_path="query.jpg",
            top_k=5
        )
        print(f"✅ Found {len(results['results'])} matches")
        for match in results['results']:
            print(f"  - {match['person_id']}: {match['similarity']:.3f}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
```

## 错误处理最佳实践

### 1. 检查响应码

```python
response = requests.post(url, json=data)
result = response.json()

if result['code'] == 0:
    # 成功
    data = result['data']
    process_data(data)
else:
    # 失败
    print(f"Error {result['code']}: {result['message']}")
    print(f"Request ID: {result['request_id']}")
```

### 2. 错误分类处理

```python
def handle_response(result):
    code = result['code']
    
    if code == 0:
        return result['data']
    
    # 按错误类型处理
    if 2000 <= code < 3000:
        # 应用相关错误
        print(f"Application error: {result['message']}")
    elif 3000 <= code < 4000:
        # 人脸相关错误
        print(f"Face error: {result['message']}")
    else:
        # 通用错误
        print(f"Error: {result['message']}")
    
    return None
```

### 3. 使用 request_id 追踪问题

```python
import logging

logger = logging.getLogger(__name__)

try:
    result = client.register_face(...)
    if result['code'] != 0:
        logger.error(
            f"Face registration failed: {result['message']} "
            f"(request_id: {result['request_id']})"
        )
except Exception as e:
    logger.exception("Unexpected error during face registration")
```

## 优势总结

### 1. 统一性
- ✅ 所有 API 使用相同的响应格式
- ✅ HTTP 状态码统一为 200
- ✅ 错误处理逻辑统一

### 2. 可追踪性
- ✅ 每个请求都有唯一的 request_id
- ✅ 便于日志追踪和问题定位
- ✅ 支持分布式追踪

### 3. 易于集成
- ✅ 客户端代码简单统一
- ✅ 不需要处理多种 HTTP 状态码
- ✅ 错误信息结构化

### 4. 向后兼容
- ✅ 添加新字段不影响现有客户端
- ✅ 错误码体系易于扩展
- ✅ 保持 API 稳定性

## 相关文档

- [API 使用指南](API_USAGE.md)
- [API 迁移指南](API_MIGRATION.md)
- [快速开始](QUICKSTART.md)

## 总结

统一的响应格式带来了：

✅ **一致性** - 所有接口返回相同结构  
✅ **可预测性** - 客户端处理逻辑统一  
✅ **可追踪性** - request_id 支持问题定位  
✅ **易维护性** - 集中的错误码管理  
✅ **易扩展性** - 灵活的 data 字段设计

立即开始使用统一响应格式，享受规范化 API 的便利！🚀
