# 依赖管理说明

## 概述

本项目采用不同的包管理策略：
- **本地开发**：使用 `uv`（快速、现代化的 Python 包管理器）
- **Docker 部署**：使用 `pip`（稳定、兼容性好）

## 为什么这样设计？

### 本地开发使用 uv
- ⚡ **速度快**：安装依赖比 pip 快 10-100 倍
- 🔧 **现代化**：更好的依赖解析和版本管理
- 💻 **开发友好**：更快的迭代和测试周期

### Docker 使用 pip
- ✅ **稳定可靠**：久经考验的包管理工具
- 🐳 **广泛兼容**：所有 Python Docker 镜像都内置
- 📦 **无需额外安装**：减少镜像大小和构建时间
- 🔒 **生产就绪**：在生产环境中更加稳定

## 使用方法

### 本地开发环境

```bash
# 1. 安装 uv
pip install uv

# 2. 创建虚拟环境
uv venv

# 3. 激活虚拟环境
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 4. 安装依赖
uv pip install -e .

# 5. 启动开发服务器
uvicorn app.main:app --reload
```

### Docker 部署

```bash
# Docker 会自动使用 pip 安装依赖
docker-compose up -d
```

## 文件说明

- `pyproject.toml` - 项目配置和依赖定义（主文件）
- `requirements.txt` - 从 pyproject.toml 生成，用于 Docker
- `Dockerfile` - 使用 `pip install -e .` 安装依赖

## 添加新依赖

### 方法 1：修改 pyproject.toml（推荐）

```toml
[project]
dependencies = [
    "fastapi>=0.109.0",
    "your-new-package>=1.0.0",  # 添加这里
]
```

然后：
```bash
# 本地开发
uv pip install -e .

# 更新 requirements.txt（可选，用于确保 Docker 同步）
pip freeze > requirements.txt

# Docker 会在下次构建时自动安装
docker-compose build
```

### 方法 2：直接安装（临时）

```bash
# 本地开发
uv pip install package-name

# 记得添加到 pyproject.toml 以便其他人使用
```

## 开发依赖

开发专用的依赖（如测试工具）定义在 `pyproject.toml` 的 `[tool.uv]` 部分：

```toml
[tool.uv]
dev-dependencies = [
    "pytest>=7.4.4",
    "pytest-asyncio>=0.23.3",
    "httpx>=0.26.0",
]
```

安装开发依赖：
```bash
uv pip install -e ".[dev]"
```

## 常见问题

### Q: 为什么要维护 requirements.txt？
A: 虽然 Dockerfile 可以直接从 pyproject.toml 安装，但 requirements.txt 提供了更快的构建速度和更好的缓存。

### Q: 如何同步两边的依赖？
A: pyproject.toml 是唯一的真实来源。requirements.txt 是从它生成的，确保两者一致。

### Q: 我可以只用 pip 吗？
A: 当然可以！用 `pip install -e .` 替代 `uv pip install -e .` 即可。

### Q: Docker 能用 uv 吗？
A: 可以，但会增加镜像大小和构建时间，在生产环境中使用 pip 更稳定。

## 最佳实践

1. ✅ **本地开发始终用 uv**（快速迭代）
2. ✅ **生产部署始终用 Docker + pip**（稳定可靠）
3. ✅ **依赖定义写在 pyproject.toml**（单一数据源）
4. ✅ **定期更新 requirements.txt**（保持同步）
5. ✅ **锁定版本号**（避免意外升级）

## 迁移指南

如果你想完全使用 uv（包括 Docker）：

```dockerfile
# Dockerfile
FROM python:3.11-slim

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 使用 uv 安装
RUN uv pip install --system -e .
```

如果你想完全使用 pip（包括本地开发）：

```bash
# 本地开发
pip install -e .
```

## 参考资料

- [uv 文档](https://github.com/astral-sh/uv)
- [pip 文档](https://pip.pypa.io/)
- [pyproject.toml 规范](https://peps.python.org/pep-0621/)
