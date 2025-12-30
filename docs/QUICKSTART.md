# 快速开始指南 (Quick Start Guide)

## 项目概述

这是一个基于 FastAPI 和 PostgreSQL + pgvector 的人脸识别服务器，提供人脸检测、特征提取、人脸检索等功能。

## 功能特性

- ✅ 应用管理 (Applications Management)
- ✅ 人脸注册 (Face Registration)
- ✅ 人脸检索 (Face Search)
- ✅ 本地/云存储支持 (Local/Cloud Storage)
- ✅ 异步任务处理 (Async Task Processing with Celery)
- ✅ Docker 容器化部署 (Docker Deployment)
- ⚠️ 人脸检测模块 (Face Detection - 空方法/Empty Methods)
- ⚠️ 特征提取模块 (Feature Extraction - 空方法/Empty Methods)
- ⚠️ 人脸搜索模块 (Face Search - 空方法/Empty Methods)

## 技术栈

- **Web 框架**: FastAPI
- **数据库**: PostgreSQL + pgvector
- **缓存/消息队列**: Redis
- **任务队列**: Celery
- **ORM**: SQLAlchemy
- **数据验证**: Pydantic
- **容器化**: Docker + Docker Compose
- **包管理**: uv (本地开发) / pip (Docker)

## 项目结构

```
face-server/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── celery_app.py        # Celery 配置
│   ├── tasks.py             # 异步任务定义
│   ├── models/              # 数据库模型
│   │   ├── application.py   # Application 模型
│   │   └── face.py          # Face 模型
│   ├── schemas/             # Pydantic schemas
│   │   ├── application.py   # Application schemas
│   │   ├── face.py          # Face schemas
│   │   └── common.py        # 通用 schemas
│   ├── api/                 # API 路由
│   │   ├── applications.py  # 应用管理 API
│   │   └── faces.py         # 人脸管理 API
│   ├── services/            # 业务逻辑层
│   │   ├── application_service.py
│   │   └── face_service.py
│   └── core/                # 核心模块
│       ├── face_detector.py      # 人脸检测 (空方法)
│       ├── feature_extractor.py  # 特征提取 (空方法)
│       ├── face_searcher.py      # 人脸检索 (空方法)
│       └── storage.py            # 存储管理 (已实现)
├── alembic/                 # 数据库迁移
│   ├── versions/
│   │   └── 001_initial_migration.py
│   └── env.py
├── tests/                   # 测试文件
├── docs/                    # 文档
│   └── prd.md              # 产品需求文档
├── docker-compose.yml       # Docker Compose 配置
├── Dockerfile               # Docker 镜像定义
├── pyproject.toml           # 项目依赖
├── alembic.ini              # Alembic 配置
├── .env.example             # 环境变量示例
├── setup_dev.py             # 开发环境设置脚本
├── example_usage.py         # API 使用示例
├── Makefile                 # 常用命令快捷方式
└── README.md                # 项目说明
```

## 安装部署

### 方式一：使用 Docker Compose (推荐)

这是最简单的方式，会自动启动所有服务。

```bash
# 1. 复制环境变量配置
copy .env.example .env

# 2. 启动所有服务
docker-compose up -d

# 3. 查看服务状态
docker-compose ps

# 4. 查看日志
docker-compose logs -f face-server

# 5. 访问 API 文档
# 打开浏览器访问: http://localhost:8000/docs
```

### 方式二：本地开发模式

适合需要频繁修改代码的开发场景。

**注意：本地开发使用 uv 管理依赖，Docker 中使用 pip**

```bash
# 1. 安装 uv (用于本地开发)
pip install uv

# 2. 运行设置脚本
python setup_dev.py

# 3. 或者手动执行以下步骤：

# 创建虚拟环境
uv venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 使用 uv 安装依赖
uv pip install -e .

# 复制环境变量配置
copy .env.example .env

# 4. 启动 PostgreSQL 和 Redis (使用 Docker)
docker-compose up postgres redis -d

# 5. 运行数据库迁移
alembic upgrade head

# 6. 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 7. (可选) 在另一个终端启动 Celery Worker
celery -A app.celery_app worker --loglevel=info
```

## API 端点

**注意**: 所有 API 接口统一使用 **POST** 方法，参数通过 **JSON body** 传递。

详细的 API 使用指南请参考：[API_USAGE.md](API_USAGE.md)

### 健康检查

- `GET /` - 根路径
- `GET /health` - 健康检查

### 应用管理

- `POST /api/v1/applications/create` - 创建应用
- `POST /api/v1/applications/list` - 列出所有应用
- `POST /api/v1/applications/get` - 获取指定应用
- `POST /api/v1/applications/update` - 更新应用
- `POST /api/v1/applications/delete` - 删除应用 (软删除)

### 人脸管理

- `POST /api/v1/faces/register` - 注册人脸 (使用 base64 编码图像)
- `POST /api/v1/faces/list` - 列出人脸 (支持按应用和人员过滤)
- `POST /api/v1/faces/get` - 获取指定人脸
- `POST /api/v1/faces/delete` - 删除人脸 (软删除)
- `POST /api/v1/faces/search` - 搜索相似人脸 (使用 base64 编码图像)

## 使用示例

### 1. 使用 Python 脚本

```bash
python example_usage.py
```

### 2. 使用 curl

```bash
# 创建应用
curl -X POST "http://localhost:8000/api/v1/applications/create" \
  -H "Content-Type: application/json" \
  -d "{\"app_code\":\"my_app\",\"app_name\":\"My Application\"}"

# 列出应用
curl -X POST "http://localhost:8000/api/v1/applications/list" \
  -H "Content-Type: application/json" \
  -d "{\"skip\":0,\"limit\":10}"

# 注册人脸 (需要图片文件)
curl -X POST "http://localhost:8000/api/v1/faces" \
  -F "app_id=YOUR_APP_ID" \
  -F "person_id=person_001" \
  -F "image=@path/to/image.jpg" \
  -F "metadata={\"name\":\"John Doe\"}"

# 搜索人脸
curl -X POST "http://localhost:8000/api/v1/faces/search" \
  -F "app_id=YOUR_APP_ID" \
  -F "image=@path/to/query.jpg" \
  -F "top_k=10" \
  -F "threshold=0.6"
```

### 3. 使用 Swagger UI

访问 http://localhost:8000/docs 可以在浏览器中直接测试 API。

## 数据库结构

### applications 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| app_code | String(100) | 应用编码 (唯一) |
| app_name | String(200) | 应用名称 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |
| deleted_at | DateTime | 删除时间 (软删除) |
| is_deleted | Boolean | 是否已删除 |

### faces 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| app_id | UUID | 应用 ID (外键) |
| person_id | String(100) | 人员 ID |
| feature_vector | Vector(512) | 特征向量 (512维) |
| image_url | String(500) | 图片 URL |
| metadata | JSONB | 元数据 (JSON格式) |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |
| deleted_at | DateTime | 删除时间 (软删除) |
| is_deleted | Boolean | 是否已删除 |

## 开发指南

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行测试并生成覆盖率报告
pytest tests/ -v --cov=app --cov-report=html
```

### 数据库迁移

```bash
# 创建新的迁移
alembic revision --autogenerate -m "描述迁移内容"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

### 代码格式化

```bash
# 格式化代码
black app/ tests/
isort app/ tests/

# 代码检查
ruff app/ tests/
```

## 实现人脸识别功能

目前人脸相关模块（检测、特征提取、搜索）都是空方法。要实现完整功能，需要：

### 1. 安装 InsightFace

```bash
pip install insightface onnxruntime
```

### 2. 实现 FaceDetector

在 [app/core/face_detector.py](app/core/face_detector.py) 中实现：
- `load_model()` - 加载人脸检测模型
- `detect()` - 检测人脸并返回边界框

### 3. 实现 FeatureExtractor

在 [app/core/feature_extractor.py](app/core/feature_extractor.py) 中实现：
- `load_model()` - 加载特征提取模型
- `extract()` - 提取512维特征向量

### 4. 实现 FaceSearcher

在 [app/core/face_searcher.py](app/core/face_searcher.py) 中实现：
- `search()` - 使用 pgvector 进行向量相似度搜索
- `calculate_similarity()` - 计算特征向量相似度

### 5. 更新 API 路由

在 [app/api/faces.py](app/api/faces.py) 中：
- 取消注释 TODO 部分
- 调用实际的检测和提取方法

## 常见问题

### Q: 如何更改数据库连接？

A: 编辑 `.env` 文件中的 `DATABASE_URL` 或相关数据库配置项。

### Q: 如何更改存储方式？

A: 在 `.env` 文件中设置 `STORAGE_TYPE=local` 或 `STORAGE_TYPE=cloud`。

### Q: 如何添加新的 API 端点？

A: 
1. 在 `app/schemas/` 中定义请求/响应模型
2. 在 `app/services/` 中实现业务逻辑
3. 在 `app/api/` 中创建路由
4. 在 `app/main.py` 中注册路由

### Q: 数据库迁移失败怎么办？

A: 
```bash
# 检查数据库连接
docker-compose ps

# 确保 pgvector 扩展已安装
docker-compose exec postgres psql -U faceserver -d faceserver -c "CREATE EXTENSION IF NOT EXISTS vector;"

# 重新运行迁移
alembic upgrade head
```

## 生产部署建议

1. **使用环境变量管理敏感信息**
2. **配置 HTTPS**
3. **设置数据库连接池**
4. **启用日志记录和监控**
5. **配置反向代理 (Nginx)**
6. **使用云存储服务 (S3/OSS)**
7. **配置 Celery 多个 Worker**
8. **设置自动备份策略**

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
