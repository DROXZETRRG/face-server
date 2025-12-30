# 依赖管理配置更新说明

## 更新内容

已将项目配置为：**本地开发使用 uv，Docker 部署使用 pip**

## 修改的文件

### 1. Dockerfile ✅
- **移除**：uv 安装步骤
- **修改**：使用 `pip install --no-cache-dir -e .` 替代 `uv pip install`
- **优势**：减少镜像大小，提高构建稳定性

### 2. requirements.txt ✅ (新增)
- **内容**：从 pyproject.toml 生成的依赖列表
- **用途**：方便 Docker 构建和其他需要 requirements.txt 的场景
- **说明**：可选文件，Docker 直接使用 pyproject.toml

### 3. README.md ✅
- **更新**：本地开发说明，强调使用 uv
- **补充**：技术栈部分添加包管理说明

### 4. docs/QUICKSTART.md ✅
- **更新**：本地开发模式说明
- **强调**：本地用 uv，Docker 用 pip
- **完善**：技术栈列表

### 5. docs/PROJECT_SUMMARY.md ✅
- **新增**：技术亮点中添加依赖管理说明
- **说明**：不同环境使用不同工具的优势

### 6. PROJECT_STATUS.md ✅
- **更新**：技术栈部分

### 7. setup_dev.py ✅
- **添加**：提示信息说明使用 uv
- **完善**：错误提示更清晰

### 8. Makefile ✅
- **新增**：`make install-dev` 命令
- **新增**：`make up-build` 命令
- **新增**：`make help` 命令显示所有可用命令

### 9. docs/DEPENDENCY_MANAGEMENT.md ✅ (新增)
- **完整的依赖管理文档**
- 为什么这样设计
- 使用方法
- 常见问题
- 最佳实践

### 10. docs/DEV_VS_DOCKER.md ✅ (新增)
- **本地 vs Docker 对比**
- 快速参考表
- 工作流示例
- 常用命令
- 故障排除

## 使用方法

### 本地开发（使用 uv）

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

或使用 Makefile：
```bash
make install        # 安装依赖
make install-dev    # 安装开发依赖
make dev            # 启动开发服务器
```

### Docker 部署（使用 pip）

```bash
# 方式 1：使用 docker-compose
docker-compose up -d

# 方式 2：使用 Makefile
make up             # 启动服务
make up-build       # 重新构建并启动
make logs           # 查看日志
make down           # 停止服务
```

## 优势说明

### 为什么本地用 uv？
- ⚡ **速度快**：安装依赖比 pip 快 10-100 倍
- 🚀 **开发效率**：快速迭代，快速测试
- 🔧 **现代化**：更好的依赖解析
- 💡 **用户体验**：响应快，等待时间短

### 为什么 Docker 用 pip？
- ✅ **稳定可靠**：Python 官方包管理器
- 🐳 **原生支持**：Docker Python 镜像内置
- 📦 **镜像更小**：无需安装额外工具
- 🔒 **生产就绪**：久经考验的生产环境工具
- 🌐 **兼容性好**：所有 Python 版本都支持

## 配置文件说明

### pyproject.toml（主配置）
```toml
[project]
dependencies = [
    # 生产依赖
]

[tool.uv]
dev-dependencies = [
    # 开发依赖
]
```

### Dockerfile（生产配置）
```dockerfile
# 使用 pip 安装
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .
```

### requirements.txt（辅助文件）
- 从 pyproject.toml 生成
- 用于 Docker 构建缓存优化
- 可选，Docker 可直接使用 pyproject.toml

## 工作流程

### 日常开发流程
1. 本地使用 uv 快速开发
2. 提交代码到版本控制
3. Docker 自动构建（使用 pip）
4. 部署到生产环境

### 添加依赖流程
1. 编辑 pyproject.toml
2. 本地运行 `uv pip install -e .`
3. 测试功能
4. 提交代码
5. Docker 重新构建（自动使用 pip）

## 常见问题

### Q: 我必须用 uv 吗？
**A:** 不是必须的。如果你更喜欢 pip，可以在本地也使用 `pip install -e .`，完全兼容。

### Q: requirements.txt 必须吗？
**A:** 不是必须的。Dockerfile 直接使用 pyproject.toml。requirements.txt 只是为了方便某些场景。

### Q: 如何保持两边同步？
**A:** pyproject.toml 是唯一的真实来源。所有依赖都定义在这里，uv 和 pip 都会读取它。

### Q: Docker 能用 uv 吗？
**A:** 可以，但会增加镜像大小。生产环境推荐使用 pip。

## 验证配置

### 验证本地开发
```bash
# 1. 创建环境
uv venv
.venv\Scripts\activate

# 2. 安装依赖
uv pip install -e .

# 3. 检查安装
python -c "import fastapi; print('FastAPI installed:', fastapi.__version__)"

# 4. 启动服务
uvicorn app.main:app --reload
# 访问 http://localhost:8000/docs
```

### 验证 Docker 部署
```bash
# 1. 构建镜像
docker-compose build

# 2. 启动服务
docker-compose up -d

# 3. 检查服务
curl http://localhost:8000/health

# 4. 查看日志
docker-compose logs face-server
```

## 迁移建议

如果你有现有项目想采用这种方式：

1. **添加 pyproject.toml**（如果没有）
2. **更新 Dockerfile** 使用 pip
3. **本地安装 uv** 并使用它
4. **测试两种环境** 确保都能正常工作
5. **更新文档** 告知团队成员

## 参考文档

- [docs/DEPENDENCY_MANAGEMENT.md](DEPENDENCY_MANAGEMENT.md) - 完整依赖管理指南
- [docs/DEV_VS_DOCKER.md](DEV_VS_DOCKER.md) - 本地 vs Docker 对比
- [docs/QUICKSTART.md](QUICKSTART.md) - 快速开始指南

## 总结

✅ **本地开发**：使用 uv，快速高效
✅ **Docker 部署**：使用 pip，稳定可靠
✅ **配置统一**：pyproject.toml 是唯一数据源
✅ **文档完善**：提供详细的使用说明
✅ **灵活选择**：开发者可根据偏好选择工具

这种配置既保证了开发效率，又确保了生产稳定性！🎉
