# API 规范统一说明

## 变更概述

为了提供更统一、更规范的 API 接口，我们对所有 API 端点进行了重构：

**核心变更**:
- ✅ 所有接口统一使用 **POST** 方法
- ✅ 所有参数通过 **JSON body** 传递
- ✅ 图像数据使用 **Base64** 编码传递
- ✅ 路径参数改为请求体参数
- ✅ 查询参数改为请求体参数

## 变更对比

### 应用管理 API

| 功能 | 旧接口 | 新接口 |
|------|--------|--------|
| 创建应用 | `POST /applications` | `POST /applications/create` |
| 列出应用 | `GET /applications?skip=0&limit=100` | `POST /applications/list` + JSON body |
| 获取应用 | `GET /applications/{app_id}` | `POST /applications/get` + JSON body |
| 更新应用 | `PUT /applications/{app_id}` | `POST /applications/update` + JSON body |
| 删除应用 | `DELETE /applications/{app_id}` | `POST /applications/delete` + JSON body |

### 人脸管理 API

| 功能 | 旧接口 | 新接口 |
|------|--------|--------|
| 注册人脸 | `POST /faces` (multipart/form-data) | `POST /faces/register` (JSON + base64) |
| 列出人脸 | `GET /faces?app_id=xxx&person_id=xxx` | `POST /faces/list` + JSON body |
| 获取人脸 | `GET /faces/{face_id}` | `POST /faces/get` + JSON body |
| 删除人脸 | `DELETE /faces/{face_id}` | `POST /faces/delete` + JSON body |
| 搜索人脸 | `POST /faces/search` (multipart/form-data) | `POST /faces/search` (JSON + base64) |

## 详细变更示例

### 示例 1: 列出应用

**旧接口**:
```bash
# GET 请求，参数在 URL 中
curl "http://localhost:8000/api/v1/applications?skip=0&limit=10"
```

**新接口**:
```bash
# POST 请求，参数在 JSON body 中
curl -X POST "http://localhost:8000/api/v1/applications/list" \
  -H "Content-Type: application/json" \
  -d '{
    "skip": 0,
    "limit": 10
  }'
```

---

### 示例 2: 获取应用

**旧接口**:
```bash
# GET 请求，app_id 在 URL 路径中
curl "http://localhost:8000/api/v1/applications/123e4567-e89b-12d3-a456-426614174000"
```

**新接口**:
```bash
# POST 请求，app_id 在 JSON body 中
curl -X POST "http://localhost:8000/api/v1/applications/get" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "123e4567-e89b-12d3-a456-426614174000"
  }'
```

---

### 示例 3: 更新应用

**旧接口**:
```bash
# PUT 请求，app_id 在路径中，更新数据在 body 中
curl -X PUT "http://localhost:8000/api/v1/applications/123e4567-e89b-12d3-a456-426614174000" \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "新名称"
  }'
```

**新接口**:
```bash
# POST 请求，app_id 和更新数据都在 JSON body 中
curl -X POST "http://localhost:8000/api/v1/applications/update" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "123e4567-e89b-12d3-a456-426614174000",
    "app_name": "新名称"
  }'
```

---

### 示例 4: 删除应用

**旧接口**:
```bash
# DELETE 请求，app_id 在路径中
curl -X DELETE "http://localhost:8000/api/v1/applications/123e4567-e89b-12d3-a456-426614174000"
```

**新接口**:
```bash
# POST 请求，app_id 在 JSON body 中
curl -X POST "http://localhost:8000/api/v1/applications/delete" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "123e4567-e89b-12d3-a456-426614174000"
  }'
```

---

### 示例 5: 注册人脸

**旧接口**:
```bash
# multipart/form-data 上传文件
curl -X POST "http://localhost:8000/api/v1/faces" \
  -F "app_id=123e4567-e89b-12d3-a456-426614174000" \
  -F "person_id=person_001" \
  -F "image=@face.jpg" \
  -F "metadata={\"name\":\"张三\"}"
```

**新接口**:
```bash
# JSON 请求，图像使用 base64 编码
IMAGE_BASE64=$(base64 -w 0 face.jpg)

curl -X POST "http://localhost:8000/api/v1/faces/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"app_id\": \"123e4567-e89b-12d3-a456-426614174000\",
    \"person_id\": \"person_001\",
    \"image_base64\": \"$IMAGE_BASE64\",
    \"metadata\": {
      \"name\": \"张三\"
    }
  }"
```

**Python 示例对比**:

**旧接口**:
```python
import requests

# 使用文件上传
with open("face.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/faces",
        files={"image": f},
        data={
            "app_id": "123e4567-e89b-12d3-a456-426614174000",
            "person_id": "person_001",
            "metadata": '{"name": "张三"}'
        }
    )
```

**新接口**:
```python
import base64
import requests

# 使用 base64 编码
with open("face.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode()

response = requests.post(
    "http://localhost:8000/api/v1/faces/register",
    json={
        "app_id": "123e4567-e89b-12d3-a456-426614174000",
        "person_id": "person_001",
        "image_base64": image_base64,
        "metadata": {
            "name": "张三"
        }
    }
)
```

---

### 示例 6: 列出人脸

**旧接口**:
```bash
# GET 请求，参数在 URL 中
curl "http://localhost:8000/api/v1/faces?app_id=123e4567-e89b-12d3-a456-426614174000&person_id=person_001&skip=0&limit=10"
```

**新接口**:
```bash
# POST 请求，参数在 JSON body 中
curl -X POST "http://localhost:8000/api/v1/faces/list" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "123e4567-e89b-12d3-a456-426614174000",
    "person_id": "person_001",
    "skip": 0,
    "limit": 10
  }'
```

---

### 示例 7: 搜索人脸

**旧接口**:
```bash
# multipart/form-data 上传文件
curl -X POST "http://localhost:8000/api/v1/faces/search" \
  -F "app_id=123e4567-e89b-12d3-a456-426614174000" \
  -F "image=@query.jpg" \
  -F "top_k=10" \
  -F "threshold=0.7" \
  -F "metadata_filter={\"department\":\"技术部\"}"
```

**新接口**:
```bash
# JSON 请求，图像使用 base64 编码
IMAGE_BASE64=$(base64 -w 0 query.jpg)

curl -X POST "http://localhost:8000/api/v1/faces/search" \
  -H "Content-Type: application/json" \
  -d "{
    \"app_id\": \"123e4567-e89b-12d3-a456-426614174000\",
    \"image_base64\": \"$IMAGE_BASE64\",
    \"top_k\": 10,
    \"threshold\": 0.7,
    \"metadata_filter\": {
      \"department\": \"技术部\"
    }
  }"
```

## 变更优势

### 1. 统一性
- ✅ 所有接口使用相同的 HTTP 方法（POST）
- ✅ 所有参数使用相同的传递方式（JSON body）
- ✅ 减少学习成本，提高开发效率

### 2. 结构化
- ✅ 复杂参数易于组织（如嵌套对象、数组）
- ✅ 类型安全，Pydantic 自动验证
- ✅ 更好的 IDE 支持和代码补全

### 3. 可扩展性
- ✅ 添加新参数不影响接口签名
- ✅ 向后兼容更容易实现
- ✅ 支持更复杂的数据结构

### 4. 安全性
- ✅ 敏感信息不会出现在 URL 中
- ✅ 不会被浏览器历史记录、日志等记录
- ✅ 更适合加密和签名

### 5. 规范性
- ✅ 符合现代 API 设计最佳实践
- ✅ 与主流框架和工具链兼容
- ✅ 更好的 OpenAPI/Swagger 文档支持

## 迁移指南

### 客户端代码迁移步骤

#### 1. 更新 URL 端点

```python
# 旧
url = f"{base_url}/applications"
url = f"{base_url}/applications/{app_id}"

# 新
url = f"{base_url}/applications/list"
url = f"{base_url}/applications/get"
```

#### 2. 更新请求方法

```python
# 旧
response = requests.get(url, params=params)
response = requests.put(url, json=data)
response = requests.delete(url)

# 新 - 统一使用 POST
response = requests.post(url, json=data)
```

#### 3. 更新参数传递方式

```python
# 旧 - URL 参数
params = {"app_id": app_id, "skip": 0, "limit": 10}
response = requests.get(url, params=params)

# 新 - JSON body
data = {"app_id": app_id, "skip": 0, "limit": 10}
response = requests.post(url, json=data)
```

#### 4. 更新文件上传

```python
# 旧 - multipart/form-data
with open("face.jpg", "rb") as f:
    files = {"image": f}
    data = {"app_id": app_id, "person_id": person_id}
    response = requests.post(url, files=files, data=data)

# 新 - base64 编码
import base64
with open("face.jpg", "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode()
data = {
    "app_id": app_id,
    "person_id": person_id,
    "image_base64": image_base64
}
response = requests.post(url, json=data)
```

### 完整迁移示例

**旧版本客户端**:
```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

class OldClient:
    def list_applications(self, skip=0, limit=100):
        response = requests.get(
            f"{BASE_URL}/applications",
            params={"skip": skip, "limit": limit}
        )
        return response.json()
    
    def get_application(self, app_id):
        response = requests.get(f"{BASE_URL}/applications/{app_id}")
        return response.json()
    
    def update_application(self, app_id, app_name):
        response = requests.put(
            f"{BASE_URL}/applications/{app_id}",
            json={"app_name": app_name}
        )
        return response.json()
    
    def register_face(self, app_id, person_id, image_path):
        with open(image_path, "rb") as f:
            response = requests.post(
                f"{BASE_URL}/faces",
                files={"image": f},
                data={"app_id": app_id, "person_id": person_id}
            )
        return response.json()
```

**新版本客户端**:
```python
import base64
import requests

BASE_URL = "http://localhost:8000/api/v1"

class NewClient:
    def list_applications(self, skip=0, limit=100):
        response = requests.post(
            f"{BASE_URL}/applications/list",
            json={"skip": skip, "limit": limit}
        )
        return response.json()
    
    def get_application(self, app_id):
        response = requests.post(
            f"{BASE_URL}/applications/get",
            json={"app_id": app_id}
        )
        return response.json()
    
    def update_application(self, app_id, app_name):
        response = requests.post(
            f"{BASE_URL}/applications/update",
            json={"app_id": app_id, "app_name": app_name}
        )
        return response.json()
    
    def register_face(self, app_id, person_id, image_path):
        with open(image_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode()
        
        response = requests.post(
            f"{BASE_URL}/faces/register",
            json={
                "app_id": app_id,
                "person_id": person_id,
                "image_base64": image_base64
            }
        )
        return response.json()
```

## 常见问题

### Q1: 为什么使用 base64 编码图像而不是文件上传？

**A**: 使用 base64 编码的优势：
- ✅ 统一使用 JSON 格式，保持 API 一致性
- ✅ 更容易与其他系统集成（如 JavaScript 前端）
- ✅ 不需要处理 multipart/form-data 的复杂性
- ✅ 更容易添加签名和加密

### Q2: base64 编码会增加数据大小吗？

**A**: 是的，base64 编码会增加约 33% 的数据大小。但考虑到：
- 对于人脸图像（通常 < 1MB），影响可接受
- 可以使用 gzip 压缩传输，减少实际传输大小
- 统一性和易用性的收益大于这个成本

### Q3: 如何优化大图像的传输？

**A**: 建议：
1. 在客户端压缩图像（如调整分辨率到 640x640）
2. 使用 JPEG 格式，适当降低质量（如 85%）
3. 启用 HTTP 压缩（gzip）
4. 对于批量操作，考虑使用异步任务

### Q4: 旧版 API 还能使用吗？

**A**: 不能。为了保持代码库简洁和一致性，旧版 API 已完全移除。
请按照本文档迁移到新版 API。

### Q5: 如何处理 URL 长度限制？

**A**: 使用 POST + JSON body 后，不再有 URL 长度限制问题，因为：
- 所有参数都在请求体中
- HTTP body 大小限制通常为几 MB
- 可以传递任意复杂的数据结构

## 相关文档

- [API 使用指南](API_USAGE.md) - 详细的 API 调用示例
- [快速开始](QUICKSTART.md) - 项目快速上手
- [人脸引擎指南](FACE_ENGINE_GUIDE.md) - 人脸引擎使用说明

## 总结

API 规范统一后：

✅ **更简单** - 统一的调用方式，降低学习成本  
✅ **更安全** - 敏感信息不暴露在 URL 中  
✅ **更灵活** - 支持复杂数据结构，易于扩展  
✅ **更规范** - 符合现代 API 设计最佳实践  
✅ **更易用** - 更好的类型安全和文档支持

立即开始使用新版 API，享受统一规范带来的便利！🚀
