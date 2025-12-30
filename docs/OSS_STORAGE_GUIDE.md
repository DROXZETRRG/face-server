# 阿里云 OSS 存储配置指南

本指南介绍如何配置项目使用阿里云 OSS 作为文件存储后端。

## 📋 功能特性

- ✅ 支持阿里云 OSS 对象存储
- ✅ 自动文件上传和管理
- ✅ 支持自定义域名
- ✅ 完整的错误处理和日志
- ✅ 统一的存储接口，轻松切换存储后端

## 🔧 配置步骤

### 1. 获取阿里云 OSS 凭证

1. 登录 [阿里云控制台](https://oss.console.aliyun.com/)
2. 创建 OSS Bucket（建议设置为私有读写）
3. 获取 AccessKey ID 和 AccessKey Secret：
   - 访问 [RAM 访问控制](https://ram.console.aliyun.com/)
   - 创建用户并授予 OSS 权限
   - 获取 AccessKey

### 2. 配置环境变量

在项目根目录的 `.env` 文件中添加：

```bash
# 设置存储类型为 OSS
STORAGE_TYPE=oss

# 阿里云 OSS 配置
OSS_ACCESS_KEY_ID=your_access_key_id_here
OSS_ACCESS_KEY_SECRET=your_access_key_secret_here
OSS_BUCKET_NAME=your-bucket-name
OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
OSS_DOMAIN=  # 可选: 自定义域名
```

### 3. OSS Endpoint 说明

根据您的 Bucket 所在地域选择对应的 Endpoint：

| 地域 | Endpoint |
|------|----------|
| 华东1（杭州） | oss-cn-hangzhou.aliyuncs.com |
| 华东2（上海） | oss-cn-shanghai.aliyuncs.com |
| 华北1（青岛） | oss-cn-qingdao.aliyuncs.com |
| 华北2（北京） | oss-cn-beijing.aliyuncs.com |
| 华北3（张家口） | oss-cn-zhangjiakou.aliyuncs.com |
| 华南1（深圳） | oss-cn-shenzhen.aliyuncs.com |
| 华南2（河源） | oss-cn-heyuan.aliyuncs.com |
| 西南1（成都） | oss-cn-chengdu.aliyuncs.com |
| 中国（香港） | oss-cn-hongkong.aliyuncs.com |

更多地域请参考：[OSS 访问域名](https://help.aliyun.com/document_detail/31837.html)

### 4. 配置自定义域名（可选）

如果您为 OSS Bucket 绑定了自定义域名：

```bash
OSS_DOMAIN=cdn.yourdomain.com
```

这样生成的文件 URL 将使用自定义域名：
- 默认: `https://your-bucket.oss-cn-hangzhou.aliyuncs.com/faces/xxx.jpg`
- 自定义: `https://cdn.yourdomain.com/faces/xxx.jpg`

## 🚀 使用示例

### 代码中使用

存储管理器会自动根据配置选择 OSS 后端：

```python
from app.core.storage import storage_manager

# 上传文件
with open("face.jpg", "rb") as f:
    file_path = storage_manager.save(f, "face.jpg", folder="faces")
    print(f"文件已上传: {file_path}")

# 获取文件 URL
url = storage_manager.get_url(file_path)
print(f"访问地址: {url}")

# 检查文件是否存在
exists = storage_manager.exists(file_path)
print(f"文件存在: {exists}")

# 删除文件
deleted = storage_manager.delete(file_path)
print(f"删除成功: {deleted}")
```

### API 调用

人脸注册 API 会自动将图片上传到 OSS：

```bash
curl -X POST "http://localhost:8000/api/v1/faces/register" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "your-app-id",
    "person_id": "p001",
    "image_base64": "base64_encoded_image...",
    "metadata": {"name": "张三"}
  }'
```

返回的 `image_url` 将是 OSS 上的文件地址。

## 🔐 安全建议

1. **权限最小化**
   - 为应用创建专用的 RAM 子账号
   - 只授予必要的 OSS 权限（PutObject, GetObject, DeleteObject）

2. **Bucket 访问控制**
   - 建议将 Bucket 设置为私有
   - 如需公开访问，配置防盗链和访问控制

3. **凭证安全**
   - 不要将 AccessKey 提交到版本控制系统
   - 使用环境变量或密钥管理服务
   - 定期轮换 AccessKey

4. **跨域配置**
   - 如果前端需要直接访问 OSS，配置 CORS 规则
   - 在 OSS 控制台 → Bucket → 权限管理 → 跨域设置

## 📊 存储后端对比

| 特性 | Local | OSS | S3 |
|------|-------|-----|-----|
| **成本** | 无额外费用 | 按量付费 | 按量付费 |
| **可靠性** | 依赖服务器 | 99.9999999999% | 99.999999999% |
| **扩展性** | 受限于磁盘 | 无限扩展 | 无限扩展 |
| **性能** | 最快 | 快 | 快 |
| **CDN** | 需自建 | 内置 CDN | 支持 CloudFront |
| **适用场景** | 开发测试 | 生产环境 | AWS 生态 |

## 🔄 切换存储后端

### 从 Local 切换到 OSS

1. 修改 `.env` 文件：
   ```bash
   STORAGE_TYPE=oss  # 从 local 改为 oss
   ```

2. 重启服务：
   ```bash
   uvicorn app.main:app --reload
   ```

3. 新上传的文件将自动存储到 OSS

### 迁移已有文件

如需迁移已有的本地文件到 OSS：

```python
import os
from pathlib import Path
from app.core.storage import LocalStorage, OSSStorage

# 初始化两个存储后端
local = LocalStorage()
oss = OSSStorage()

# 遍历本地文件
storage_path = Path("./storage/faces")
for file_path in storage_path.glob("*.jpg"):
    with open(file_path, "rb") as f:
        # 上传到 OSS
        oss_key = oss.save(f, file_path.name, folder="faces")
        print(f"迁移: {file_path.name} -> {oss_key}")
```

## 🐛 故障排查

### 1. 认证失败

**错误**: `AccessDenied` 或 `InvalidAccessKeyId`

**解决方案**:
- 检查 AccessKey ID 和 Secret 是否正确
- 确认 RAM 用户有 OSS 权限
- 检查 IP 白名单限制

### 2. Bucket 不存在

**错误**: `NoSuchBucket`

**解决方案**:
- 确认 Bucket 名称正确
- 检查 Endpoint 是否与 Bucket 地域匹配
- 确认 Bucket 已创建

### 3. 权限不足

**错误**: `AccessForbidden`

**解决方案**:
- 为 RAM 用户添加 `AliyunOSSFullAccess` 或自定义权限策略
- 检查 Bucket 策略设置

### 4. 网络问题

**错误**: 连接超时或网络错误

**解决方案**:
- 检查服务器网络配置
- 确认可以访问阿里云 OSS 服务
- 如在内网，使用内网 Endpoint（如 `oss-cn-hangzhou-internal.aliyuncs.com`）

## 📖 相关文档

- [阿里云 OSS 官方文档](https://help.aliyun.com/product/31815.html)
- [Python SDK 文档](https://help.aliyun.com/document_detail/32026.html)
- [OSS 最佳实践](https://help.aliyun.com/document_detail/31867.html)

## 💡 提示

1. **开发环境**：建议使用 `local` 存储，无需额外配置
2. **生产环境**：建议使用 `oss` 存储，提供更好的可靠性和扩展性
3. **混合部署**：可以在不同环境使用不同的存储配置
4. **成本优化**：
   - 启用 OSS 生命周期管理，自动删除或归档旧文件
   - 使用低频访问或归档存储类型降低成本
   - 开启 OSS 图片处理服务，减少传输流量
