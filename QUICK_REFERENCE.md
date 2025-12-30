# 快速参考卡片

## 🚀 本地开发（使用 uv）

```bash
# 安装 uv
pip install uv

# 创建环境并安装依赖
uv venv
.venv\Scripts\activate
uv pip install -e .

# 启动开发服务器
uvicorn app.main:app --reload

# 或使用 Makefile
make install        # 安装依赖
make dev           # 启动服务
```

**为什么用 uv？**
⚡ 速度快 10-100 倍 | 🔄 快速迭代 | 💻 现代化工具

---

## 🐳 Docker 部署（使用 pip）

```bash
# 一键启动所有服务
docker-compose up -d

# 或使用 Makefile
make up            # 启动服务
make up-build      # 重新构建并启动
make logs          # 查看日志
```

**为什么用 pip？**
✅ 稳定可靠 | 📦 镜像更小 | 🔒 生产就绪

---

## 📝 添加依赖

```bash
# 1. 编辑 pyproject.toml
[project]
dependencies = [
    "new-package>=1.0.0",  # 添加这里
]

# 2. 本地安装（快速）
uv pip install -e .

# 3. Docker 重新构建
docker-compose build
```

---

## 🔧 常用命令

### Makefile 快捷命令
```bash
make help          # 显示所有命令
make install       # 安装依赖（uv）
make install-dev   # 安装开发依赖
make dev           # 启动开发服务器
make up            # 启动 Docker 服务
make down          # 停止 Docker 服务
make test          # 运行测试
make migrate       # 数据库迁移
```

### 数据库操作
```bash
# 本地
alembic upgrade head          # 应用迁移
alembic revision --autogenerate -m "msg"  # 创建迁移

# Docker
docker-compose exec face-server alembic upgrade head
```

---

## 📚 文档链接

- [QUICKSTART.md](docs/QUICKSTART.md) - 快速开始
- [DEPENDENCY_MANAGEMENT.md](docs/DEPENDENCY_MANAGEMENT.md) - 依赖管理详解
- [DEV_VS_DOCKER.md](docs/DEV_VS_DOCKER.md) - 开发 vs Docker 对比
- [CHANGELOG_DEPENDENCY.md](CHANGELOG_DEPENDENCY.md) - 更新说明

---

## ⚡ 核心理念

| 环境 | 工具 | 优势 |
|-----|------|------|
| 本地开发 | uv | 快速、高效、现代 |
| Docker 部署 | pip | 稳定、可靠、生产 |
| 配置管理 | pyproject.toml | 统一、简洁、标准 |

**一个配置文件，两种安装方式，完美平衡！** 🎯
