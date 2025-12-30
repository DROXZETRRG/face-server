# 本地开发 vs Docker 部署对比

## 快速参考

| 环境 | 包管理器 | 安装命令 | 优势 |
|------|---------|---------|------|
| **本地开发** | uv | `uv pip install -e .` | ⚡ 快速安装，快速迭代 |
| **Docker 部署** | pip | `pip install -e .` | ✅ 稳定可靠，生产就绪 |

## 详细对比

### 本地开发环境

```bash
# 安装 uv
pip install uv

# 创建虚拟环境
uv venv
.venv\Scripts\activate

# 安装依赖（快速）
uv pip install -e .

# 启动开发服务器
uvicorn app.main:app --reload
```

**特点：**
- ⚡ 安装速度极快（10-100倍）
- 🔄 快速迭代和测试
- 💻 适合频繁修改代码
- 🛠️ 现代化的依赖解析

### Docker 部署

```bash
# 构建镜像（自动使用 pip）
docker-compose build

# 启动服务
docker-compose up -d
```

**Dockerfile 关键部分：**
```dockerfile
# 使用 pip 安装（稳定）
RUN pip install --no-cache-dir -e .
```

**特点：**
- ✅ 久经考验，稳定可靠
- 🐳 Docker 原生支持
- 📦 无需额外工具
- 🔒 生产环境首选

## 工作流示例

### 场景 1：添加新功能

```bash
# 1. 本地开发（使用 uv）
uv venv && .venv\Scripts\activate
uv pip install -e .

# 2. 修改代码并测试
uvicorn app.main:app --reload

# 3. 提交代码
git add .
git commit -m "Add new feature"

# 4. Docker 部署（使用 pip）
docker-compose build
docker-compose up -d
```

### 场景 2：添加新依赖

```bash
# 1. 编辑 pyproject.toml
[project]
dependencies = [
    "new-package>=1.0.0",
]

# 2. 本地安装（快速测试）
uv pip install -e .

# 3. 验证功能正常
python -c "import new_package; print('OK')"

# 4. 重新构建 Docker
docker-compose build
```

## 文件说明

### pyproject.toml（主配置文件）
```toml
[project]
dependencies = [
    "fastapi>=0.109.0",
    # ... 所有依赖
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.4.4",
    # ... 开发依赖
]
```

### Dockerfile（Docker 配置）
```dockerfile
# 使用 pip（不需要 uv）
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .
```

### requirements.txt（可选）
```txt
# 从 pyproject.toml 生成
# 用于加速 Docker 构建缓存
fastapi>=0.109.0
...
```

## 常用命令

### 本地开发

```bash
# 创建环境
uv venv

# 激活环境
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 安装依赖
uv pip install -e .

# 安装开发依赖
uv pip install -e ".[dev]"

# 运行服务
uvicorn app.main:app --reload

# 运行测试
pytest

# 数据库迁移
alembic upgrade head
```

### Docker 部署

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重新构建并启动
docker-compose up -d --build

# 进入容器
docker-compose exec face-server bash

# 运行迁移
docker-compose exec face-server alembic upgrade head
```

## 故障排除

### 本地开发问题

**问题：uv 安装失败**
```bash
# 方案 1：更新 pip
pip install --upgrade pip

# 方案 2：使用 pip 替代
pip install -e .
```

**问题：虚拟环境激活失败**
```bash
# Windows PowerShell 执行策略
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 或使用 cmd
.venv\Scripts\activate.bat
```

### Docker 部署问题

**问题：依赖安装失败**
```bash
# 清理缓存重新构建
docker-compose build --no-cache
```

**问题：容器启动失败**
```bash
# 查看详细日志
docker-compose logs face-server

# 检查容器状态
docker-compose ps
```

## 推荐工作流

### 日常开发
1. 使用 uv 在本地快速开发和测试
2. 提交代码到 Git
3. 使用 Docker 进行集成测试
4. 部署到生产环境（Docker）

### 持续集成
1. CI 管道使用 Docker 构建
2. 自动化测试在 Docker 容器中运行
3. 部署到生产环境

## 总结

- 🏠 **本地开发**：uv - 快速、高效、现代化
- 🚀 **生产部署**：pip - 稳定、可靠、久经考验
- 📝 **配置管理**：pyproject.toml - 单一数据源
- 🔄 **最佳实践**：根据场景选择合适的工具
