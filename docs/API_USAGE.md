# API 使用指南

## 概述

所有 API 接口统一使用 **POST** 方法，参数通过 **JSON body** 传递。这种设计具有以下优势：

- ✅ **统一规范** - 所有接口使用相同的调用方式
- ✅ **参数结构化** - 复杂参数易于组织和验证
- ✅ **易于扩展** - 添加新参数不影响接口签名
- ✅ **安全性更好** - 敏感信息不会出现在 URL 中
- ✅ **支持复杂数据** - JSON 可以表达嵌套和数组结构

## Base URL

```
http://localhost:8000/api/v1
```

## 通用响应格式

### 成功响应

```json
{
  "id": "uuid",
  "field1": "value1",
  "field2": "value2"
}
```

### 错误响应

```json
{
  "detail": "错误描述信息"
}
```

## 应用管理 API

### 1. 创建应用

**接口**: `POST /applications/create`

**请求体**:
```json
{
  "app_code": "my_app",
  "app_name": "我的应用"
}
```

**响应**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "app_code": "my_app",
  "app_name": "我的应用",
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z"
}
```

**curl 示例**:
```bash
curl -X POST "http://localhost:8000/api/v1/applications/create" \
  -H "Content-Type: application/json" \
  -d '{
    "app_code": "my_app",
    "app_name": "我的应用"
  }'
```

**Python 示例**:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/applications/create",
    json={
        "app_code": "my_app",
        "app_name": "我的应用"
    }
)
app = response.json()
print(f"Created app: {app['id']}")
```

---

### 2. 查询应用列表

**接口**: `POST /applications/list`

**请求体**:
```json
{
  "skip": 0,
  "limit": 100
}
```

**响应**:
```json
{
  "total": 10,
  "items": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "app_code": "my_app",
      "app_name": "我的应用",
      "created_at": "2025-12-30T10:00:00Z",
      "updated_at": "2025-12-30T10:00:00Z"
    }
  ]
}
```

**curl 示例**:
```bash
curl -X POST "http://localhost:8000/api/v1/applications/list" \
  -H "Content-Type: application/json" \
  -d '{
    "skip": 0,
    "limit": 10
  }'
```

**Python 示例**:
```python
response = requests.post(
    "http://localhost:8000/api/v1/applications/list",
    json={"skip": 0, "limit": 10}
)
data = response.json()
print(f"Total: {data['total']}")
for app in data['items']:
    print(f"- {app['app_name']}: {app['id']}")
```

---

### 3. 获取应用详情

**接口**: `POST /applications/get`

**请求体**:
```json
{
  "app_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

**响应**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "app_code": "my_app",
  "app_name": "我的应用",
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z"
}
```

**curl 示例**:
```bash
curl -X POST "http://localhost:8000/api/v1/applications/get" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "123e4567-e89b-12d3-a456-426614174000"
  }'
```

---

### 4. 更新应用

**接口**: `POST /applications/update`

**请求体**:
```json
{
  "app_id": "123e4567-e89b-12d3-a456-426614174000",
  "app_name": "新的应用名称"
}
```

**响应**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "app_code": "my_app",
  "app_name": "新的应用名称",
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T11:00:00Z"
}
```

**curl 示例**:
```bash
curl -X POST "http://localhost:8000/api/v1/applications/update" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "123e4567-e89b-12d3-a456-426614174000",
    "app_name": "新的应用名称"
  }'
```

---

### 5. 删除应用

**接口**: `POST /applications/delete`

**请求体**:
```json
{
  "app_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

**响应**: HTTP 204 No Content

**curl 示例**:
```bash
curl -X POST "http://localhost:8000/api/v1/applications/delete" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "123e4567-e89b-12d3-a456-426614174000"
  }'
```

---

## 人脸管理 API

### 1. 注册人脸

**接口**: `POST /faces/register`

**请求体**:
```json
{
  "app_id": "123e4567-e89b-12d3-a456-426614174000",
  "person_id": "person_001",
  "image_base64": "/9j/4AAQSkZJRgABAQAAAQ...",
  "metadata": {
    "name": "张三",
    "department": "技术部",
    "employee_id": "EMP001"
  }
}
```

**参数说明**:
- `app_id`: 应用 ID (UUID)
- `person_id`: 人员标识符
- `image_base64`: Base64 编码的人脸图像
- `metadata`: 可选的元数据（JSON 对象）

**响应**:
```json
{
  "id": "face-uuid",
  "app_id": "123e4567-e89b-12d3-a456-426614174000",
  "person_id": "person_001",
  "image_url": "http://storage.example.com/faces/abc123.jpg",
  "metadata": {
    "name": "张三",
    "department": "技术部",
    "employee_id": "EMP001"
  },
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z"
}
```

**Python 示例**:
```python
import base64
import requests

# 读取图像并转换为 base64
with open("face.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode()

response = requests.post(
    "http://localhost:8000/api/v1/faces/register",
    json={
        "app_id": "123e4567-e89b-12d3-a456-426614174000",
        "person_id": "person_001",
        "image_base64": image_base64,
        "metadata": {
            "name": "张三",
            "department": "技术部"
        }
    }
)

face = response.json()
print(f"Face registered: {face['id']}")
print(f"Image URL: {face['image_url']}")
```

**curl 示例**:
```bash
# 将图像转换为 base64
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

---

### 2. 查询人脸列表

**接口**: `POST /faces/list`

**请求体**:
```json
{
  "app_id": "123e4567-e89b-12d3-a456-426614174000",
  "person_id": "person_001",
  "skip": 0,
  "limit": 100
}
```

**参数说明**:
- `app_id`: 应用 ID (必填)
- `person_id`: 人员 ID 过滤 (可选)
- `skip`: 跳过记录数 (默认: 0)
- `limit`: 返回记录数 (默认: 100)

**响应**:
```json
{
  "total": 5,
  "items": [
    {
      "id": "face-uuid",
      "app_id": "123e4567-e89b-12d3-a456-426614174000",
      "person_id": "person_001",
      "image_url": "http://storage.example.com/faces/abc123.jpg",
      "metadata": {
        "name": "张三"
      },
      "created_at": "2025-12-30T10:00:00Z",
      "updated_at": "2025-12-30T10:00:00Z"
    }
  ]
}
```

**Python 示例**:
```python
response = requests.post(
    "http://localhost:8000/api/v1/faces/list",
    json={
        "app_id": "123e4567-e89b-12d3-a456-426614174000",
        "person_id": "person_001",
        "skip": 0,
        "limit": 10
    }
)

data = response.json()
print(f"Total faces: {data['total']}")
for face in data['items']:
    print(f"- {face['person_id']}: {face['id']}")
```

---

### 3. 获取人脸详情

**接口**: `POST /faces/get`

**请求体**:
```json
{
  "face_id": "face-uuid"
}
```

**响应**:
```json
{
  "id": "face-uuid",
  "app_id": "123e4567-e89b-12d3-a456-426614174000",
  "person_id": "person_001",
  "image_url": "http://storage.example.com/faces/abc123.jpg",
  "metadata": {
    "name": "张三"
  },
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z"
}
```

---

### 4. 删除人脸

**接口**: `POST /faces/delete`

**请求体**:
```json
{
  "face_id": "face-uuid"
}
```

**响应**: HTTP 204 No Content

---

### 5. 搜索人脸

**接口**: `POST /faces/search`

**请求体**:
```json
{
  "app_id": "123e4567-e89b-12d3-a456-426614174000",
  "image_base64": "/9j/4AAQSkZJRgABAQAAAQ...",
  "top_k": 10,
  "threshold": 0.7,
  "metadata_filter": {
    "department": "技术部"
  }
}
```

**参数说明**:
- `app_id`: 应用 ID (必填)
- `image_base64`: Base64 编码的查询图像 (必填)
- `top_k`: 返回结果数量 (1-100, 默认: 10)
- `threshold`: 相似度阈值 (0.0-1.0, 默认: 0.6)
- `metadata_filter`: 元数据过滤器 (可选)

**响应**:
```json
{
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
}
```

**Python 示例**:
```python
import base64
import requests

# 读取查询图像
with open("query.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode()

response = requests.post(
    "http://localhost:8000/api/v1/faces/search",
    json={
        "app_id": "123e4567-e89b-12d3-a456-426614174000",
        "image_base64": image_base64,
        "top_k": 5,
        "threshold": 0.7,
        "metadata_filter": {
            "department": "技术部"
        }
    }
)

result = response.json()
print(f"Query time: {result['query_time_ms']:.2f}ms")
print(f"Found {len(result['results'])} matches:")

for match in result['results']:
    print(f"- {match['person_id']}: {match['similarity']:.3f}")
    if match['metadata']:
        print(f"  Name: {match['metadata'].get('name')}")
```

**完整示例 - 人脸识别流程**:
```python
import base64
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 1. 创建应用
app_response = requests.post(
    f"{BASE_URL}/applications/create",
    json={
        "app_code": "attendance_system",
        "app_name": "考勤系统"
    }
)
app_id = app_response.json()["id"]
print(f"✅ Created app: {app_id}")

# 2. 注册人脸
def register_face(image_path, person_id, name):
    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode()
    
    response = requests.post(
        f"{BASE_URL}/faces/register",
        json={
            "app_id": app_id,
            "person_id": person_id,
            "image_base64": image_base64,
            "metadata": {"name": name}
        }
    )
    return response.json()

# 注册多个人脸
face1 = register_face("employee1.jpg", "EMP001", "张三")
face2 = register_face("employee2.jpg", "EMP002", "李四")
print(f"✅ Registered 2 faces")

# 3. 搜索人脸
with open("query.jpg", "rb") as f:
    query_base64 = base64.b64encode(f.read()).decode()

search_response = requests.post(
    f"{BASE_URL}/faces/search",
    json={
        "app_id": app_id,
        "image_base64": query_base64,
        "top_k": 1,
        "threshold": 0.7
    }
)

result = search_response.json()
if result['results']:
    match = result['results'][0]
    print(f"✅ Matched: {match['metadata']['name']} (similarity: {match['similarity']:.3f})")
else:
    print("❌ No match found")

# 4. 查询人脸列表
list_response = requests.post(
    f"{BASE_URL}/faces/list",
    json={
        "app_id": app_id,
        "skip": 0,
        "limit": 10
    }
)
print(f"✅ Total faces: {list_response.json()['total']}")
```

---

## 错误处理

### 常见错误码

| 状态码 | 说明 |
|-------|------|
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

### 错误响应示例

**404 Not Found**:
```json
{
  "detail": "Application with ID '123e4567-e89b-12d3-a456-426614174000' not found"
}
```

**400 Bad Request**:
```json
{
  "detail": "No face detected in the image"
}
```

**Python 错误处理**:
```python
try:
    response = requests.post(
        "http://localhost:8000/api/v1/faces/register",
        json=request_data
    )
    response.raise_for_status()  # 抛出 HTTP 错误
    result = response.json()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 404:
        print("应用不存在")
    elif e.response.status_code == 400:
        print(f"请求错误: {e.response.json()['detail']}")
    else:
        print(f"HTTP 错误: {e}")
except Exception as e:
    print(f"请求失败: {e}")
```

---

## 图像处理

### Base64 编码

**Python**:
```python
import base64

# 编码
with open("image.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode()

# 解码
image_data = base64.b64decode(image_base64)
with open("output.jpg", "wb") as f:
    f.write(image_data)
```

**JavaScript**:
```javascript
// Node.js 编码
const fs = require('fs');
const imageBase64 = fs.readFileSync('image.jpg').toString('base64');

// 浏览器编码 (从文件输入)
const input = document.querySelector('input[type="file"]');
input.addEventListener('change', (e) => {
  const file = e.target.files[0];
  const reader = new FileReader();
  reader.onload = (event) => {
    const imageBase64 = event.target.result.split(',')[1];
    console.log(imageBase64);
  };
  reader.readAsDataURL(file);
});
```

**命令行**:
```bash
# Linux/Mac
base64 -w 0 image.jpg

# Windows PowerShell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("image.jpg"))
```

---

## 最佳实践

### 1. 图像要求
- **格式**: JPG, PNG, BMP
- **最小尺寸**: 100x100 像素
- **最大尺寸**: 4000x4000 像素
- **文件大小**: < 10MB
- **人脸要求**: 正面、清晰、光线充足

### 2. 性能优化
- 使用适当的 `limit` 值进行分页
- 使用 `metadata_filter` 减少搜索范围
- 批量操作使用合理的并发数
- 缓存应用 ID 避免重复查询

### 3. 安全建议
- 使用 HTTPS 传输
- 实现 API 认证和授权
- 限制请求频率
- 验证和清理用户输入
- 不在日志中记录敏感数据

### 4. 错误处理
- 始终检查 HTTP 状态码
- 解析错误响应的 `detail` 字段
- 实现重试机制（指数退避）
- 记录错误以便调试

---

## 测试工具

### Postman Collection

可以导入以下 Postman Collection 进行测试：

```json
{
  "info": {
    "name": "Face Recognition API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Create Application",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/applications/create",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"app_code\": \"test_app\",\n  \"app_name\": \"测试应用\"\n}"
        }
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000/api/v1"
    }
  ]
}
```

### Swagger UI

访问自动生成的 API 文档：
```
http://localhost:8000/docs
```

---

## 总结

统一使用 POST + JSON body 的 API 设计提供了：

✅ **一致性** - 所有接口遵循相同模式  
✅ **可维护性** - 易于理解和维护  
✅ **可扩展性** - 轻松添加新参数  
✅ **类型安全** - Pydantic 自动验证  
✅ **文档完善** - OpenAPI 自动生成文档

立即开始使用这些 API 构建您的人脸识别应用！🚀
