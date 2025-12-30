# 人脸识别服务器

基于 FastAPI、PostgreSQL + pgvector 和 InsightFace 构建的高性能人脸识别服务器。

## ✨ 功能特性

- 🎯 **人脸检测** - 使用 InsightFace buffalo_l 模型进行高精度人脸检测
- 🔍 **特征提取** - 提取 512 维人脸特征向量
- 🔎 **人脸搜索** - 基于 pgvector 的高效相似度搜索
- 📱 **应用管理** - 多应用隔离，支持多租户场景
- 💾 **灵活存储** - 支持本地存储、阿里云 OSS、AWS S3
- 🚀 **实时检测** - WebSocket 实时人脸识别，支持二进制传输优化
- 🎨 **交互式演示** - 内置演示页面，支持摄像头抓拍和实时识别
- 🐳 **容器化部署** - 完整的 Docker 和 Docker Compose 支持

## 🛠️ 技术栈

- **后端框架**: FastAPI 0.109.0+
- **数据库**: PostgreSQL + pgvector（向量搜索）
- **人脸引擎**: InsightFace 0.7.3 (buffalo_l 模型)
- **存储**: 本地文件系统 / 阿里云 OSS / AWS S3
- **部署**: Docker / Docker Compose
- **包管理**: uv (开发) / pip (生产)
- **数据库迁移**: Alembic
- **Python**: 3.9+

## 🚀 快速开始

### 前置要求

- Docker 和 Docker Compose
- Python 3.9+ (本地开发)
- uv (Python 包管理器，推荐)

### 方式一：使用 Docker Compose（推荐）

1. **克隆仓库**
```bash
git clone https://github.com/lihongjie0209/face-server.git
cd face-server
```

2. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，根据需要调整配置
```

3. **启动服务**
```bash
docker-compose up -d
```

4. **运行数据库迁移**
```bash
docker-compose exec face-server alembic upgrade head
```

5. **访问服务**
   - API 地址: http://localhost:8000
   - Swagger 文档: http://localhost:8000/docs
   - 演示页面: http://localhost:8000/static/demo.html

### 方式二：本地开发

1. **安装 uv**
```bash
pip install uv
```

2. **创建虚拟环境并安装依赖**
```bash
uv venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
uv pip install -e .
```

3. **启动 PostgreSQL（使用 Docker）**
```bash
docker-compose -f docker-compose.dev.yml up -d
```

4. **运行数据库迁移**
```bash
alembic upgrade head
```

5. **启动服务**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. **访问演示页面**
   - 浏览器打开: http://localhost:8000/static/demo.html

## 📖 API 接口

### 应用管理

- `POST /api/v1/applications/create` - 创建应用
- `POST /api/v1/applications/list` - 获取应用列表
- `POST /api/v1/applications/get` - 获取应用详情
- `POST /api/v1/applications/update` - 更新应用
- `POST /api/v1/applications/delete` - 删除应用

### 人脸管理

- `POST /api/v1/faces/register` - 注册人脸
- `POST /api/v1/faces/list` - 获取人脸列表
- `POST /api/v1/faces/get` - 获取人脸详情
- `POST /api/v1/faces/delete` - 删除人脸
- `POST /api/v1/faces/search` - 搜索人脸（1:N 识别）

### 实时检测

- `WebSocket /ws/detect` - WebSocket 实时人脸检测

## 🎯 使用示例

### 1. 创建应用
```bash
curl -X POST "http://localhost:8000/api/v1/applications/create" \
  -H "Content-Type: application/json" \
  -d '{
    "app_code": "demo_app",
    "app_name": "演示应用",
    "description": "人脸识别演示"
  }'
```

### 2. 注册人脸
```bash
curl -X POST "http://localhost:8000/api/v1/faces/register" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "your-app-id",
    "person_id": "p001",
    "image_base64": "base64_encoded_image_here",
    "metadata": {"name": "张三", "department": "技术部"}
  }'
```

### 3. 搜索人脸
```bash
curl -X POST "http://localhost:8000/api/v1/faces/search" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "your-app-id",
    "image_base64": "base64_encoded_query_image",
    "top_k": 5,
    "threshold": 0.6
  }'
```

详细 API 文档请访问: http://localhost:8000/docs

## 📁 项目结构

```
face-server/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── models/              # SQLAlchemy 数据模型
│   │   ├── application.py   # 应用模型
│   │   └── face.py          # 人脸模型
│   ├── schemas/             # Pydantic 数据模式
│   │   ├── application.py   # 应用 Schema
│   │   ├── face.py          # 人脸 Schema
│   │   └── common.py        # 公共 Schema
│   ├── api/                 # API 路由
│   │   ├── applications.py  # 应用接口
│   │   ├── faces.py         # 人脸接口
│   │   └── websocket.py     # WebSocket 接口
│   ├── services/            # 业务逻辑层
│   │   ├── application_service.py
│   │   └── face_service.py
│   ├── core/                # 核心模块
│   │   ├── face_engine.py   # InsightFace 引擎
│   │   └── storage.py       # 存储引擎（本地/OSS/S3）
│   ├── static/              # 静态文件
│   │   └── demo.html        # 演示页面
│   └── utils/               # 工具函数
├── alembic/                 # 数据库迁移
│   └── versions/            # 迁移脚本
├── docs/                    # 文档
│   ├── API_USAGE.md         # API 使用文档
│   ├── DEMO_GUIDE.md        # 演示指南
│   ├── OSS_STORAGE_GUIDE.md # OSS 存储配置
│   └── ...
├── tests/                   # 测试文件
├── storage/                 # 本地文件存储
├── docker-compose.yml       # Docker Compose 配置
├── docker-compose.dev.yml   # 开发环境配置
├── Dockerfile               # Docker 镜像
├── pyproject.toml           # 项目依赖
├── .env.example             # 环境变量示例
└── README.md                # 项目说明
```

## ⚙️ 配置说明

### 数据库配置
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/faceserver
```

### 存储配置

**本地存储（开发环境）**
```bash
STORAGE_TYPE=local
LOCAL_STORAGE_PATH=./storage
```

**阿里云 OSS（生产推荐）**
```bash
STORAGE_TYPE=oss
OSS_ACCESS_KEY_ID=your_access_key_id
OSS_ACCESS_KEY_SECRET=your_access_key_secret
OSS_BUCKET_NAME=your-bucket-name
OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
```

详细配置请查看: [docs/OSS_STORAGE_GUIDE.md](docs/OSS_STORAGE_GUIDE.md)

### 人脸引擎配置
```bash
FACE_MODEL_PACK=buffalo_l      # 模型: buffalo_l/buffalo_s/antelopev2
FACE_DET_SIZE=(640, 640)       # 检测尺寸
FACE_DET_THRESH=0.5            # 检测阈值
FACE_DEVICE=cpu                # 设备: cpu/cuda
```

## 📚 文档

- [快速开始](docs/QUICKSTART.md) - 详细的入门指南
- [API 使用](docs/API_USAGE.md) - API 接口详细说明
- [演示指南](docs/DEMO_GUIDE.md) - 演示页面使用教程
- [OSS 存储配置](docs/OSS_STORAGE_GUIDE.md) - 阿里云 OSS 配置指南
- [InsightFace 指南](docs/INSIGHTFACE_GUIDE.md) - 人脸引擎配置说明

## 🎨 功能特色

### 🖥️ 交互式演示页面

内置完整的演示页面，支持：
- ✅ 摄像头实时检测
- ✅ 人脸抓拍注册
- ✅ 自动递增员工 ID (p1, p2, p3...)
- ✅ 实时识别结果展示
- ✅ 可调节采样频率和识别阈值
- ✅ WebSocket 二进制传输优化（节省 33% 带宽）

### 📊 性能优化

- **向量搜索**: 使用 pgvector 进行高效的相似度搜索
- **二进制传输**: WebSocket 使用二进制传输，减少带宽占用
- **缓存策略**: 人脸特征向量缓存
- **异步处理**: FastAPI 异步接口，高并发支持

## 🔧 开发指南

### 运行测试
```bash
pytest tests/
```

### 添加数据库迁移
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### 代码格式化
```bash
black app/
isort app/
```

## 🐛 故障排查

遇到问题？查看我们的故障排查指南：
- [数据库连接问题](docs/TROUBLESHOOTING.md#database)
- [InsightFace 模型下载](docs/TROUBLESHOOTING.md#model-download)
- [OSS 配置问题](docs/OSS_STORAGE_GUIDE.md#故障排查)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
